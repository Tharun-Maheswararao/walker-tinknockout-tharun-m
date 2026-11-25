# FRICTIONAL — final project pitch (A8)

*Dated entries. Claude records the facts of what happened, with commits and files; every "In my words" line is Tharun's, and Claude leaves it blank.*

## 2026-11-23 — reading the handout

- **What happened:** read the A8 handout. Claude listed what already exists, by tag. It found no export preset and no build; the project's Forward+ renderer rules out a web build without the Compatibility renderer; and the local Brutalist checkout has no `show-tell` skill.
- **In my words:** I understood A8 to be asking for an honest pitch of what the final project will be, with what already exists kept separate from what is only planned. What surprised me was realizing that Forward+ ruled out a web export without switching renderers, and that we didn't have a standalone export preset configured yet.

## 2026-11-24 — choosing the project

- **What happened:**
  - **Options:** Claude offered three directions that fit the existing tags: a vertical slice, a technical-art pack, or a gameplay system. I chose (c), the gameplay system.
  - **A new game:** I asked whether to make a new game. Claude pointed to the handout ("lives in your walker- repository") and the A7 rule that the one allowed change of game had to happen before Assignment 4, and recommended staying with Tin Knockout. I stayed.
  - **The facts file:** Claude wrote `pitch/EXISTS-FACTS.md`.
  - **My answers:** the comparables (Street Fighter 6 and Tekken 8, both games I have played), the target role (gameplay programmer), the export target (macOS desktop) and "a mix" for why.
  - **The brief:** Claude drafted `pitch/PROJECT-BRIEF.md` from these.
- **In my words:** I chose the gameplay system because deterministic frame-data, input buffering, and state-machine mechanics match my target gameplay programmer role and the fighting games I play. Staying with Tin Knockout made sense once I saw the repository rules, and building on top of verified tags `a2` through `a7` gave the pitch concrete mechanical proof instead of starting over.

## 2026-11-24 — reviewing the brief

- **What happened:** Tharun read the draft brief and approved it without changes, in chat ("Reviewed, start the film"). The pitch folder was committed and the film session started.
- **In my words:** I checked that the brief's scope claims, comparables, and test counts matched the verified facts in `EXISTS-FACTS.md` and didn't overpromise unbuilt features before approving it.

## 2026-11-24 — the film

- **What happened:**
  - **The build:** a separate Claude Code session built the film from the brief with the Brutalist toolkit. It made real Movie Maker captures from an isolated copy of tag `a7`, re-ran the tests on a clean copy (pins 49, structure 57, edges 70, 0 failed), and took four renders: one render-integrity report refused a render, which was fixed and re-rendered (`gate-reports/REPORT-render1-REFUSED.md`). The final gate showed 0 blocker and 0 major defects (`gate-reports/REPORT.md`).
  - **The master:** 3:41, SHA-256 `190ed4b2…2cdc`.
  - **Claude's check of the narration:** it is honest, with one wording slip in B03, "opens on its fifth tick" (it is tick 5 counted from 0).
  - **Upload:** Tharun uploaded the master to Google Drive and gave the link.
- **In my words:** I watched the full 3:41 master and verified that the scripted-input captures and test-count claims matched tag `a7`, and that the training room and overlay were labelled as proposals. The pacing and technical breakdown came across clearly, and the "fifth tick" phrasing in B03 doesn't bother me since the visual and underlying tick-5 data are accurate, so I'm leaving it as is.
