"""Generate sound effects (AudioLDM 2) and music (MusicGen-small) locally and log
every run to tools/gen/gen-log.jsonl, the same log as the image generator.

  python tools/gen/gen_audio.py sfx   --id SFX-JAB   --seeds 1-4 --seconds 2  --prompt "..."
  python tools/gen/gen_audio.py music --id MUS-WALTZ --seeds 1-3 --seconds 30 --prompt "..."

Raw WAVs go to raw/<ID>/ (git-ignored). Trimming, loop cutting and OGG export
are separate, logged edit steps (tools/edit/).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "tools" / "gen" / "gen-log.jsonl"
MODELS = {
    "sfx": ("cvssp/audioldm2", "c8e7e189d324425c05c4c2f81214041ef4107983"),
    "music": ("facebook/musicgen-small", "4c8334b02c6ec4e8664a91979669a501ec497792"),
}


def seeds_of(s: str) -> list[int]:
    out: list[int] = []
    for part in s.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["sfx", "music"])
    ap.add_argument("--id", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--negative", default="low quality, noise, speech, music" )
    ap.add_argument("--seeds", default="1-4")
    ap.add_argument("--seconds", type=float, default=2.0)
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--tag", default="")
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()

    repo, rev = MODELS[a.kind]
    out_dir = REPO / "raw" / a.id
    out_dir.mkdir(parents=True, exist_ok=True)

    if a.kind == "sfx":
        from diffusers import AudioLDM2Pipeline
        pipe = AudioLDM2Pipeline.from_pretrained(repo, revision=rev, torch_dtype=torch.float32).to(a.device)
        pipe.set_progress_bar_config(disable=True)
        # Compatibility patch: transformers 5 removed GenerationMixin from GPT2Model,
        # but diffusers' AudioLDM2 still calls two of its helpers on it. Bind them back.
        import types
        from transformers.generation.utils import GenerationMixin
        lm = pipe.language_model
        for name in ("_update_model_kwargs_for_generation", "_get_initial_cache_position"):
            if not hasattr(lm, name) and hasattr(GenerationMixin, name):
                setattr(lm, name, types.MethodType(getattr(GenerationMixin, name), lm))
        sr = 16000
    else:
        from transformers import AutoProcessor, MusicgenForConditionalGeneration
        proc = AutoProcessor.from_pretrained(repo, revision=rev)
        model = MusicgenForConditionalGeneration.from_pretrained(repo, revision=rev).to(a.device)
        sr = model.config.audio_encoder.sampling_rate

    tag = f"_{a.tag}" if a.tag else ""
    for seed in seeds_of(a.seeds):
        t0 = time.time()
        torch.manual_seed(seed)
        if a.kind == "sfx":
            g = torch.Generator(a.device).manual_seed(seed)
            audio = pipe(a.prompt, negative_prompt=a.negative, num_inference_steps=a.steps,
                         audio_length_in_s=a.seconds, guidance_scale=a.guidance, generator=g).audios[0]
            settings = {"steps": a.steps, "guidance_scale": a.guidance, "negative_prompt": a.negative}
        else:
            inputs = proc(text=[a.prompt], padding=True, return_tensors="pt").to(a.device)
            tokens = int(a.seconds * 50)  # MusicGen: 50 audio frames per second
            wav = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=tokens)
            audio = wav[0, 0].cpu().numpy()
            settings = {"max_new_tokens": tokens, "guidance_scale": 3.0, "do_sample": True}
        audio = np.asarray(audio, dtype=np.float32)
        path = out_dir / f"{a.id}{tag}_s{seed}.wav"
        sf.write(path, audio, sr)
        rec = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "asset_id": a.id, "model": repo, "revision": rev,
               "where": f"local {a.device} (Apple M4)", "mode": a.kind, "prompt": a.prompt, "seed": seed,
               "seconds": a.seconds, "sample_rate": sr, **settings, "tag": a.tag,
               "output": str(path.relative_to(REPO)), "gen_seconds": round(time.time() - t0, 1)}
        with LOG.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print("wrote", rec["output"], rec["gen_seconds"], "s", flush=True)


if __name__ == "__main__":
    main()
