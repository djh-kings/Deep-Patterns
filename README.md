# Deep Patterns

**An A-level / 6th-form Computer Science enrichment resource — KCS, Curiosity Day 2026.**

Deep Patterns pairs three famous paintings with the algorithms that can reproduce
their visual character, and uses each as a way into a real Computer Science idea:
algorithmic complexity, numerical simulation, and the line between what we can and
can't compute. It is the sequel to [Hidden Patterns](https://djh-kings.github.io/Hidden-Patterns/) —
where Hidden Patterns asked *can you spot the algorithm?*, Deep Patterns asks
*can you build it, explain why it scales the way it does, and find it in the real world?*

The project is a single self-contained web page backed by three standalone Python
reference simulations.

---

## The three paintings

| Painting | Artist | Algorithm | CS idea |
|----------|--------|-----------|---------|
| **The Starry Night** | Van Gogh, 1889 | Curl-noise flow field (particles advected through a divergence-free vector field) | `O(n)` advection — linear, embarrassingly parallel |
| **The Great Wave** | Hokusai, c.1831 | 2D wave equation, explicit finite-difference (Verlet) integration | `O(n)` per timestep, the Courant stability condition, and where the *linear* model stops being real physics |
| **The Scream** | Munch, 1893 | Gray-Scott reaction–diffusion (Turing patterns) | `O(n)` per step, and the unpredictable transient before a pattern emerges |

Each section of the site follows the same four-part structure: **A** the live
simulation, **B** the algorithm and its equations, **C** the complexity, and
**D** where the idea shows up in the real world.

---

## What's in this repository

```
index.html         The interactive single-page site (all HTML/CSS/JS inline,
                   three live <canvas> simulations, sliders, complexity tables)
starry_night.py    Reference simulation — curl-noise flow field (matplotlib)
great_wave.py      Reference simulation — 2D wave equation (matplotlib)
the_scream.py      Reference simulation — Gray-Scott reaction–diffusion (matplotlib)
starry-night.jpg   Painting images used on the landing cards
great-wave.jpg
the-scream.jpg
deep-patterns-corrections-and-code-prompt.md
                   Working brief: factual corrections to the copy + implementation notes
```

The **web simulations** (in `index.html`) and the **Python simulations** are
independent implementations of the same algorithms. The Python versions are
fuller, heavily commented, interactive reference programs intended for students
to read, run, and modify; the in-browser JavaScript versions are lighter and
tuned for a smooth, click-to-interact experience on the page.

---

## Running it

### The website

It's a single static file — no build step, no dependencies.

```bash
# just open it
open index.html            # macOS
xdg-open index.html        # Linux

# or serve locally (recommended, so web fonts and images load cleanly)
python3 -m http.server
# then visit http://localhost:8000
```

### The Python simulations

```bash
pip install numpy matplotlib

python starry_night.py     # curl-noise flow field
python great_wave.py       # 2D wave equation  (click to add a source, shift+click for a barrier)
python the_scream.py       # Gray-Scott reaction–diffusion (click to seed; presets at top of file)
```

Each script has a parameters block at the top you can edit, and prints its
controls on launch.

---

## The simulations in brief

- **Starry Night — curl noise.** A scalar potential field ψ(x, y, t) is built from
  layered sine waves; the particle velocity is its *curl* `(∂ψ/∂y, −∂ψ/∂x)`, which is
  divergence-free, so particles swirl and circulate rather than pile up. Each particle
  reads the field once and moves — no particle interacts with any other, which is why a
  frame is `O(n)`. (Tier 4 of the student challenge is to *add* interaction and watch it
  become `O(n²)`.)

- **The Great Wave — the wave equation.** Heights on a grid evolve under
  `∂²η/∂t² = c²∇²η`, discretised with a 5-point Laplacian and Verlet time-stepping.
  Each cell depends on its previous two states and its four neighbours. It is stable only
  while the Courant number satisfies `c·Δt/Δx ≤ 1/√2`. Importantly this is the *linear*
  wave equation — **not** the Navier–Stokes equations of real fluid flow; the site is
  careful to flag where the model stops being real physics.

- **The Scream — Gray-Scott.** Two virtual chemicals `u` and `v` diffuse at different
  rates and react (`u + 2v → 3v`), producing spontaneous spatial pattern from a nearly
  uniform start — Alan Turing's 1952 morphogenesis idea. The web version defaults to the
  self-replicating "mitosis" regime (F ≈ 0.034, k ≈ 0.064): clicking seeds a new colony
  that divides and spreads.

---

## How this was built

The page and simulations were developed iteratively with **Claude Code**. The
algorithms, copy, layout, and visual design were drafted, then refined through a
series of targeted fixes against the running page:

- The three Python reference programs and the interactive `index.html` were authored first.
- The painting photographs were wired into the landing cards.
- Several simulation bugs were diagnosed and fixed by instrumenting the actual code —
  for example the Starry Night flow was nearly invisible because each particle stepped
  only ~0.02 px/frame (a `dt` scaling error), and The Scream's click-to-seed appeared
  broken because its default feed/kill rates sat in a near-dead regime that filled the
  canvas with no room for new seeds to show. Both were verified by driving a headless
  browser and comparing before/after renders rather than by eye alone.
- The header and footer were restyled to match the Hidden Patterns site for a consistent
  brand across the two resources.
- `deep-patterns-corrections-and-code-prompt.md` captures a round of factual corrections
  to the explanatory copy (notably the Great Wave's wave-equation-vs-Navier–Stokes framing
  and tightening of the complexity tables).

---

## Credits

D. Haxton, KCS Computer Science — Curiosity Day 2026.
Paintings are public-domain works by Vincent van Gogh, Katsushika Hokusai, and Edvard Munch.
