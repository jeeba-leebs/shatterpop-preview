# Shatterpop Sound Cues v1
Style: soft, sugary, glassy, never harsh. Export OGG + M4A, 44.1 kHz, mono for SFX, peak −3 dBFS, short tails. **Originals only** (doc §11/§14). Use CC0 or royalty-free sources as *raw material*, then layer and pitch them so the result is ours, and log every source and license in the provenance log.
| # | Event | Feel | Length | Suggested source type |
|---|---|---|---|---|
| 1 | Pick up piece | Light rubbery "blip" | 80–120 ms | Self-recorded finger-on-balloon squeak, pitched up |
| 2 | Place piece | Squishy gummy "plop" (randomize pitch ±3 st) | 150–220 ms | Foley: wet sponge / jelly squeeze (record in-house, or CC0 from Freesound) |
| 3 | Invalid drop | Soft "bonk" with a downward pitch | 150 ms | Synth (sfxr/jsfxr/ChipTone, all free) |
| 4 | Row/column clear | Sparkly "pop" chime | 400–600 ms | Glockenspiel/celesta sample (CC0 or royalty-free library) + bubble pop |
| 5 | Combo step ×n | Same chime raised +2 semitones per step (cap +10) | 400 ms | Pitch-shift cue 4 at runtime |
| 6 | Gummy aging tick | Very faint frost "tink" (only at age = timer − 1) | 120 ms | Wine-glass tap, low volume |
| 7 | Crystal sets | Crystalline "ting" + freeze shimmer | 500–700 ms | Wind-chime / bowed-glass sample (CC0), reverse-swell layer |
| 8 | Crystal crack | Sharp "tick" + hairline crackle | 200–300 ms | Ice-cube crack foley (record in-house: ice in warm water) |
| 9 | Crystal shatter | Bright glass burst + chime tail | 600–900 ms | Layer: glass-break (licensed library) + celesta hit |
| 10 | Splash hit | Small droplet "plip" → tick | 200 ms | Water-drop foley, CC0 |
| 11 | Icebreaker | Hammer "clink" whoosh → shatter (9) | 700 ms | Metal-on-glass tap foley + whoosh (royalty-free) |
| 12 | Bomb | Fuse fizz → candy "boom" (rounded, no low rumble) | 900 ms | Synth boom (sfxr) + confetti popper foley |
| 13 | Hint | Warm "ding" + shimmer | 400 ms | Synth bell (free plugin, e.g. Surge XT) |
| 14 | Swap / Undo | Whoosh-rewind | 300 ms | Tape-rewind whoosh, synth |
| 15 | Near-fail panel | Gentle "uh-oh" two-note | 500 ms | Marimba sample (CC0) |
| 16 | Game over | Descending 3-note marimba + Pop flop "boing" | 1.2 s | Marimba + spring boing foley |
| 17 | Pop squeak (react) | Cute "pop!" vocalization | 150–300 ms | Record a VO actor (work-for-hire), pitched up. No TTS of real voices |
| 18 | Coin gain | Small coin tink | 150 ms | Coin foley, CC0 |
| 19 | UI tap | Soft click | 50 ms | Synth |
| 20 | Music loop (menu/run) | Bouncy lo-fi toy box, 90–100 BPM, loopable | 60–90 s | Commission or royalty-free music library (check the mobile-game license tier); keep stems for ducking |
**Mix:** duck the music −6 dB for 400 ms on shatter. Pre-decode all SFX and fire them through a single AudioContext pool. Respect the sound toggle and iOS silent-switch behavior.
