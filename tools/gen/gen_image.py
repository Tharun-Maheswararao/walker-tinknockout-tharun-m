"""Generate images with SDXL-Turbo locally (Apple Silicon / MPS) and log every
run so it can be reproduced exactly.

Every call appends one JSON line per image to tools/gen/gen-log.jsonl:
asset id, model + revision, mode, prompt, seed, steps, size, strength, init
image, output path. Full-size outputs go to raw/<ID>/ (git-ignored); accepted
images are copied into godot/assets by hand and recorded in SOURCES.md.

Examples:
  python tools/gen/gen_image.py --id CHAR-REF --seeds 1-8 --prompt "..."
  python tools/gen/gen_image.py --id CHAR-JAB --init raw/CHAR-REF/CHAR-REF_s3.png \
      --strength 0.6 --seeds 1-6 --prompt "..."
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import AutoPipelineForImage2Image, AutoPipelineForText2Image
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
LOG = REPO / "tools" / "gen" / "gen-log.jsonl"
MODEL = "stabilityai/sdxl-turbo"
REVISION = "71153311d3dbb46851df1931d3ca6e939de83304"


def parse_seeds(s: str) -> list[int]:
    out: list[int] = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--seeds", default="1-4")
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--width", type=int, default=0, help="txt2img only; default = size")
    ap.add_argument("--height", type=int, default=0)
    ap.add_argument("--init", default=None, help="init image for img2img")
    ap.add_argument("--strength", type=float, default=0.6)
    ap.add_argument("--tag", default="", help="suffix to keep prompt variants apart")
    a = ap.parse_args()

    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    kw = dict(torch_dtype=torch.float16, variant="fp16", revision=REVISION)
    if a.init:
        pipe = AutoPipelineForImage2Image.from_pretrained(MODEL, **kw).to(dev)
        init = Image.open(REPO / a.init if not Path(a.init).is_absolute() else a.init).convert("RGB").resize((a.size, a.size))
    else:
        pipe = AutoPipelineForText2Image.from_pretrained(MODEL, **kw).to(dev)
    pipe.vae.to(torch.float32)  # fp16 SDXL VAE gives black/NaN images on MPS
    pipe.set_progress_bar_config(disable=True)

    out_dir = REPO / "raw" / a.id
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"_{a.tag}" if a.tag else ""
    for seed in parse_seeds(a.seeds):
        g = torch.Generator("cpu").manual_seed(seed)
        t0 = time.time()
        if a.init:
            steps = max(a.steps, int(round(1 / a.strength + 0.5)))  # turbo img2img needs steps*strength >= 1
            img = pipe(prompt=a.prompt, image=init, strength=a.strength, num_inference_steps=steps,
                       guidance_scale=0.0, generator=g).images[0]
        else:
            steps = a.steps
            img = pipe(prompt=a.prompt, num_inference_steps=steps, guidance_scale=0.0,
                       width=a.width or a.size, height=a.height or a.size, generator=g).images[0]
        path = out_dir / f"{a.id}{tag}_s{seed}.png"
        img.save(path)
        rec = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S"), "asset_id": a.id, "model": MODEL,
            "revision": REVISION, "where": f"local {dev} (Apple M4, diffusers)",
            "mode": "img2img" if a.init else "txt2img", "prompt": a.prompt, "negative_prompt": None,
            "guidance_scale": 0.0, "seed": seed, "steps": steps, "size": [a.width or a.size, a.height or a.size],
            "strength": a.strength if a.init else None, "init": a.init, "tag": a.tag,
            "output": str(path.relative_to(REPO)), "seconds": round(time.time() - t0, 1),
        }
        with LOG.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print("wrote", rec["output"], rec["seconds"], "s", flush=True)


if __name__ == "__main__":
    main()
