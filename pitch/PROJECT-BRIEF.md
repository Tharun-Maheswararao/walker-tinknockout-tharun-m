# PROJECT-BRIEF — Tin Knockout Fighter Kit (working title)

*Tharun Maheswararao · CSYE 7270 final project pitch · 2026-11-24. Drafted by Claude from Tharun's choices (option (c), the comparables he has played, the target role, the export target, and "a mix" of new and existing skills) and from `pitch/EXISTS-FACTS.md`. Tharun is responsible for it; his review is recorded in `pitch/FRICTIONAL.md`. Past tense means it exists at the tag named; "will" means it does not exist yet.*

**1. What is it?** A fighter controller and animation state machine for Godot 4, whose every move is written in frames and pinned by tests a stranger can rerun. When it is done, it will be two things in the `walker-tinknockout-tharun-m` repository:
- a **macOS desktop build of a training room**, where you control Bolt against a dummy with a frame-data overlay;
- the **fighter as a reusable scene** (`Fighter.tscn`), with its test suite and tuning log.

**2. Why would anyone care?** In this kit, the frame data and the animation cannot drift apart without a test failing:
- the jab's 5 / 6 / 10 frames, the hitstop and every phase boundary were pinned by headless tests (`a7`);
- the animation was locked to the gameplay tick, measured at a 0 s gap;
- each new move will join the same tests.

It shows that feel can be specified in frames and checked, not only tuned by eye.

**3. What does it give the person who uses it?** A gameplay programmer or lead will be able to:
- open the build and press one key to see a move's startup, active and recovery frames drawn as they happen;
- open the repository and run one command to see the same frames confirmed by tests.

**4. What makes it different?** I have played **Street Fighter 6** and **Tekken 8**. Both are far larger, finished games, and this kit does not compete with them as a game. What they don't give is what this gives: their frame data is something the player reads, while here a programmer can **open the state machine that produces the frames and rerun the tests that prove them**. The game also has its own mechanic: a wind-up spring that every move drains and that must be rewound, leaving you open while you crank.

**5. Who opens it, and what do they do?** **Target role: gameplay programmer.** **Reader: a lead gameplay engineer or hiring manager.** In the first sixty seconds they will:
1. double-click the macOS build;
2. land in the training room, with no menu to read;
3. press J and watch the overlay count the jab's frames;
4. press K and see a cutlass's different timing.

A second path: `./scripts/run-test.sh test_a7_edges.gd 60` prints "70 checks, 0 failed" today.

**6. What does it prove about me?**
- **Animation and state:** one authority per animated node, clips synced to `state_t` (`a7`, `TEST-REPORT.md` A7-6).
- **Verification habits:**
  - pins before a change and re-pins after, identical (A7-2);
  - edge tests one tick before, on and after every boundary (A7-7);
  - mutations run in git worktrees (A7-5);
  - a seam bug that a fixture log caught after the suite passed it (A7-9a);
  - human checks recorded separately from the automated ones.
- **Profiling:** two clocks measured on an Apple M4 (A7-9e). It will add a measured frame rate for the build on that machine.
- **Shaders and particles** (`a5`, `a6`) as presentation that listens to the state machine's signals.

**Evidence it will add:** an edge suite and a tuning-log entry for every new animated move, and a test that the reusable scene keeps every pinned number.

**7. What is in, what is out, what comes first?**
- **Out:** no online or local multiplayer netcode, no second character's art, one arena only, no save system.
- **In:**
  - the reusable `Fighter.tscn`;
  - animated cutlass, block and hurt, alongside the jab;
  - a short input buffer, so a press near the end of a move is kept;
  - the frame-data overlay;
  - the training room;
  - the macOS export.
- **First:** the fighter will run as its own scene in the training room against a still dummy. Anyone will know it ran when `test_a7_pins.gd`, `test_a7_structure.gd` and `test_a7_edges.gd` give their `a7` counts (49, 57 and 70 checks, 0 failed) against the new scene, unchanged.

**What could sink it:** turning the fighter into a reusable scene means untangling it from `main.gd`, which today sets `opponent` and `spawn_cork` and calls `step()`. That refactor could silently move a frame boundary. **What I will do:** the pins already lock every boundary at 60 and 30 fps. The refactor will not be committed unless they pass with identical logs. A second, smaller risk: the project uses Forward+ on Vulkan, so the macOS build will be tested on the M4 before anything is claimed about it, and there will be no web build.

**8. Why this project?** A mix.
- **Already have, with evidence:** shaders driven by game state (`a5`), particle effects with a measured cost (`a6`), an animation state machine with pinned behaviour, edge tests and mutations (`a7`), and directing an agent with scoped plans and approvals (every `a7` commit).
- **New to me:** packaging a system as a reusable scene, an input buffer, a frame-data overlay, and a desktop export with a frame-rate measurement.
- **I don't know yet** whether an `AnimationTree` would simplify the state machine. I will find out by building the cutlass both ways in a branch and keeping whichever passes the same edge tests with fewer authorities.

## Exists today

- Playable one-round slice, title → fight → KO → rematch, Bolt vs a pattern-driven Rivet: tag `a2` (`9788922`).
- 11-state fighter state machine with the intent seam and five signals: `godot/fighter/fighter.gd` at `a7` (`a0c95cc`).
- Animated jab (cutout rig, 60 fps) and looping key cycle, one authority each: `a7`.
- Tests, 0 failed at `a7`: pins 49, structure 57, edges 70, read-backs 58 and 26, A2 slice 25.
- Tuning log with two revisions (`TUNING.md`, A7); mutations, seam fix and clock measurement (`TEST-REPORT.md`, A7).
- Shaders `a5` (`f4dda68`); particles `a6` (`66c8cbc`); a film for every tag (`README.md`).

## Will exist

- `Fighter.tscn` usable without `main.gd`, and the training room scene.
- Animated cutlass, block and hurt, each with an edge suite and a tuning entry.
- An input buffer (with its own pins), and the frame-data overlay.
- A macOS desktop export, with its frame rate measured on the Apple M4.
- An `AnimationTree` comparison on the cutlass, kept or dropped on evidence.
