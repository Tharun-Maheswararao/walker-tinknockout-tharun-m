# CONCEPT — Tin Knockout

*Version 1 · 2026-10-05 · written before any asset was generated. Later changes are appended under "Revisions", never rewritten.*

## The game in two sentences

You are **Bolt**, a tin wind-up deep-sea-diver toy who fights other tin toys at the bottom of an empty goldfish bowl on a toy-shop counter after closing time. Every punch, cutlass swing and cork-harpoon shot unwinds the spring in your back, so you win by spending wind wisely and rewinding only when it is safe.

## Core loop

| | |
|---|---|
| **Repeated action** | Close the distance → pick an attack → land it or miss → back off and hold **Rewind** to refill your spring. |
| **Decision each time** | *Which attack can my spring afford right now?* Jab is cheap, cutlass costs more but reaches further, the harpoon pop-gun costs the most but hits from across the bowl. And: *is it safe to stop and rewind?* |
| **Risk** | Rewinding locks you in place with your guard down. Let the spring run **empty** and Bolt slumps, stalled and defenceless, for a long beat. A hit while rewinding or stalled knocks you down. |

Fight shape for the slice: one round, Bolt vs **Rivet** (the same toy in copper-and-verdigris paint), first to empty the other's health bar wins.

## Design pillars

| Pillar | What it means | Visual choice that honours it | Sound choice that honours it |
|---|---|---|---|
| **1. Every move costs wind** | The spring is the whole strategy; the player must always know how much is left. | The winding key on Bolt's back is the biggest prop in his silhouette; a brass spring dial on the HUD; Bolt visibly **slumps** when empty. | Rewind is a ratchet that clicks once per quarter-turn, so you can *count* the wind going in. Empty spring is a falling *wrrr-clunk*. |
| **2. Tin you can hear** | Every contact is a material: brass, tin, cork, glass. | Painted-tin finish with rivets, seams and chipped enamel; sparks on metal-on-metal hits. | Each attack has its own material sound: jab = hollow tin *clang*, cutlass = metallic *shing*, harpoon = cork *pop*. |
| **3. Read the fight at a glance** | The fight must be readable with the sound off (assignment requirement, and good design). | One strong pose per state; Bolt's **porthole face** shows his state through the glass; hit-flash, short hitstop, screen shake; HUD dials, not tiny numbers. | Sound only *confirms* what the screen already shows; nothing is sound-only. |
| **4. Toys after closing** | Playful but a little eerie: the toys come alive only when nobody is watching. | Cool blue moonlight through the shop window, warm brass highlights, the curved glass of the bowl framing the fight. | A music-box / carnival-organ waltz that sounds like it is coming from a toy on the next shelf. |

## Art direction

**Style:** a painted, side-view illustration of mid-century lithographed tin toys: chunky proportions (Bolt's helmet is about 40 % of his height), clean dark outlines, flat enamel colours with a little wear. It serves *Tin you can hear* because the materials are obvious at a glance, and *Read the fight at a glance* because chunky toy proportions give each pose a clear silhouette. It is **not** pixel art.

**Reference notes (words, no artists):**
1. *Material:* stamped and lithographed tinplate, visible seams and tabs, rivets, enamel paint chipped at the edges to show bare metal; polished brass on the helmet.
2. *Lighting:* night shop interior, cool blue moonlight from the left, warm amber rim light from a street lamp outside, soft glass reflections.
3. *Place and era:* an old toy shop counter, mid-century; inside an empty goldfish bowl with aquarium gravel, a plastic sunken-castle ornament and plastic seaweed.

## Audio direction

The player should feel **mechanical weight with toy-box humour**: hits are solid and satisfying, but everything sounds small and made of metal, not like real violence.

| Moment | Music behaviour |
|---|---|
| Round start | Bell, then the waltz loop starts. |
| During the round | Waltz loops seamlessly. |
| Bolt's spring below 25 % | The waltz **slows and drops in pitch** like a music box winding down; it recovers as you rewind. |
| Pause | Music is muffled (low-pass) and quieter, as if heard from underwater; it returns when you unpause. |
| KO (win or lose) | Music **stops dead** with the KO bell. A short win or lose sting may follow (stretch goal). |
| End of slice | Silence after the sting; the result stays on screen until the player restarts. |

Music and effects have separate mute keys. Sound never decides game state; a muted or missing sound changes nothing that happens.

## Scope for the Assignment 2 slice

**In:** Bolt vs Rivet (pattern-driven opponent) in one arena · fists + tin cutlass + cork harpoon pop-gun · spring meter and rewind · health · KO · pause · mute.

**Out (next steps toward the full game):** real AI, more weapons (mallet, shield, spring-dart pistol), weapon pickups from the toy box, more fighters and arenas, a second human player.

## Revisions

*(none yet)*
