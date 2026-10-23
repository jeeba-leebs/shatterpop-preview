# Shatterpop FX Spec v1 (for Maker)
All timings are in ms at 60 fps. Asset paths are relative to this folder. Respect the **reduce-motion** setting: when it's on, drop shake, scale overshoot and particles to ≤25% and keep only the opacity fades. Budget: **≤150 live particles** total, pooled. Use transform/opacity only (no layout props) in CSS, and pre-tint sprites. Avoid runtime blur filters on mobile.

## Easing tokens
| Token | CSS | Use |
|---|---|---|
| `easeOutBack` | `cubic-bezier(0.34,1.56,0.64,1)` | pop-ins, bounce landings |
| `easeOutCubic` | `cubic-bezier(0.33,1,0.68,1)` | particles, shards |
| `easeInCubic` | `cubic-bezier(0.32,0,0.67,0)` | fade-outs, gravity |
| `easeInOutSine` | `cubic-bezier(0.37,0,0.63,1)` | idle wobble, glow pulse |
Phaser equivalents: `Back.Out`, `Cubic.Out`, `Cubic.In`, `Sine.InOut`.

## 1. Piece drop / bounce (squash & jelly ripple)
- Drop: each cell from its drag position to the grid, 90 ms `easeOutCubic`.
- Squash keyframes (per cell, transform-origin bottom center): 0 ms scale(1,1) → 70 ms (1.12, 0.86) → 160 ms (0.95, 1.06) → 240 ms (1.02, 0.99) → 300 ms (1,1). Use `easeOutBack` for the whole run.
- Ripple: orthogonal neighbors get the same curve at 40% amplitude, delayed 50 ms per Manhattan step (max 2 steps).
- Idle wobble on gummies: scaleY 1 → 1.015 → 1, 2400 ms `easeInOutSine` loop, with a random phase per cell. Disable under reduce-motion.
- Invalid drop: shake ±6 px x, 3 cycles, 180 ms total, then return to the tray at 220 ms `easeOutBack`.

## 2. Row/column clear sparkle
Sprites: `fx/fx_row_glow.png` (stretch along the line), `fx/fx_sparkle@*x.png`, `fx/fx_sparkle_honey@*x.png`.
| t (ms) | Event |
|---|---|
| 0 | Line glow: opacity 0→1 (60 ms), scaleY 0.3→1.2 `easeOutBack`. Cells flash white (additive overlay at 0.6 opacity) |
| 0–240 | Cells pop **staggered from the placement point outward, 25 ms per cell**: scale 1→1.18 (80 ms) → 0 (120 ms, `easeInCubic`), opacity 1→0 over the last 100 ms |
| 40 | Sparkle burst per cell: **6 particles** (+2 per combo step, cap 12; whole clear capped at 90). Speed 180–420 px/s, random angle, drag 0.92/frame, gravity +600 px/s². Life 450–700 ms. Scale 0.4→1.0 (first 20%) →0. Opacity 1 until 60% of life, then →0. Rotation ±180°/s. 30% honey tint |
| 120 | Score popup "+N": spawns at the line's center, scale 0.5→1.15→1 (220 ms `easeOutBack`), rises 80 px over 700 ms, fades over the last 250 ms |
| 260–420 | Line glow fades 1→0 `easeInCubic` |
- Combo ≥ ×2: add a 2 px screen shake (≤4 px max per doc), 120 ms, 3 oscillations. Haptic light.
- Canvas: draw the glow and sparkles with `globalCompositeOperation='lighter'`. Pre-render at 2x and draw scaled.
- CSS: `.sparkle{position:absolute;will-change:transform,opacity;mix-blend-mode:screen}` driven by the Web Animations API.

## 3. Crystal set / crack / shatter
Sprites: `crystal/crystal_intact`, `crystal/crystal_cracked`, `crystal/crystal_shatter_sheet@*x.png` (6 frames, 96 px square at 1x, horizontal; the shatter frame is **1.5× the cell size**, so center it on the cell), `fx/fx_shard`.
- **Set (gummy → crystal):** 0–200 ms frost overlay (`blocks/overlay_frost_aging`) opacity 0→1; at 200 ms cross-fade to `crystal_intact` (120 ms); scale 1→1.08→1 (260 ms `easeOutBack`); one white glint sweeps diagonally across (300 ms). Sound: `crystal_set`.
- **Aging hint:** frost overlay opacity = age / setTimer (0, .25, .5, .75), tween 200 ms.
- **Crack (2 HP → 1 HP):** 0 ms swap to `crystal_cracked` behind a white flash (opacity 0.8→0, 120 ms); hairline reveal: mask the crack lines from the center outward over 140 ms `easeOutCubic`; cell shake ±3 px, 100 ms; **4 small shards** (life 300 ms, speed 120–200 px/s). Sound: `crystal_crack`.
- **Shatter:** frames 1–6 at **50 ms per frame (300 ms total)**; hold frame 1 for an extra **33 ms (1-frame slow-mo / hit-stop for the whole board)**. Spawn **10–14 shard particles** (`fx_shard`, random tint white / #9FE0FF / #4FB4F2): speed 220–480 px/s, gravity +900 px/s², spin ±540°/s, life 500–750 ms, scale 1→0.4, opacity 1→0 over the last 40%. Expanding ring: radius 0.3→1.2 cell, stroke 5→0.5 px, opacity 0.8→0, 300 ms `easeOutCubic`. "+50" popup like §2. Shake 3 px, 100 ms. Haptic medium.
- **Splash (teach the rule):** one droplet (the popped gummy's color, 14 px) arcs from the gummy to the crystal: 180 ms, quadratic Bézier with peak −40 px, then the crack sequence.
- **Cross-clear instant shatter:** skip the crack step and use a 1.3× bigger ring plus "SHATTERED!" text.
- Readability: intact = facets + blue, cracked = white fracture star + center dot. Both read in grayscale; keep that contrast if you retint.

## 4. Glow (power-up armed, gear proc, Hint target)
- Power-up icon armed: outer glow (CSS `filter: drop-shadow(0 0 12px #FFC94D)` or a pre-rendered additive halo) with opacity pulse 0.5↔1, 900 ms `easeInOutSine`, and scale 1↔1.06.
- Hint target cells: lilac (#B79CFF) inner glow, opacity 0.35↔0.8, 700 ms loop, until a piece is picked up.
- Gear proc on Pop: radial honey glow behind the item, 0→1 (120 ms) →0 (500 ms), plus 5 honey sparkles.
- Icebreaker use: the icon flies to the target (250 ms `easeInCubic`), then the shatter sequence with +100. Neighbors take the crack sequence after a 60 ms delay.
- Bomb use: fuse sparkle 300 ms → 3×3 white flash (80 ms) → cells scale to 0 (150 ms, staggered 20 ms from the center) → 30 sparkles plus shards for any crystals → shake 4 px, 160 ms.

## 5. Pop reactions (idle/cheer art provided)
- Idle: breathing scaleY 1↔1.03, scaleX 1↔0.985, 1800 ms `easeInOutSine`; the sprout rotates ±6°.
- Cheer: swap to `pop_cheer`, jump −40 px, 260 ms `easeOutCubic`, land with a squash (1.1, 0.9) for 120 ms, then return to idle after 900 ms.

## Implementation notes
- Phaser 3: put blocks, crystals and FX in one atlas (TexturePacker or `free-tex-packer`, 2048² max, at 2x). Use `ParticleEmitter` with `blendMode: ADD` and a pooled `maxParticles`.
- Pick the asset scale by `devicePixelRatio`: <1.5 → @1x, <2.5 → @2x, else @3x. The base cell is 64 px at @1x (the board frame is laid out at 112 px per cell, so scale the frame to match your cell size; the grid pitch is 112 with a 28 px pad and a 40 px lip offset at the top).
- Canvas fallback: cache every tinted sprite in an offscreen canvas once, and never re-tint per frame.
