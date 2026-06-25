# Deep Patterns — Corrections Pack & Claude Code Prompt
### Factual fixes for the live site + implementation brief
### D. Haxton, KCS — June 2026

---

## Part 1 — Summary of all corrections

The live site at https://djh-kings.github.io/Deep-Patterns/ contains several factual and framing errors, concentrated in the Great Wave and The Scream sections. This document specifies the corrected copy. Severity order:

**Must fix (factual errors a sharp student or colleague will catch):**
1. Great Wave: "fluid surface / fluid dynamics / Navier-Stokes" framing applied to what is actually the linear wave equation — a different equation entirely.
2. Great Wave Eq. 2: garbled Laplacian symbol (`∇2h`) and missing Δx² term; doesn't match the code.
3. Great Wave: "Each cell is independent" — false; cells are coupled to their four neighbours.
4. The Scream: complexity table shows O(n log n) and O(n²) columns that nothing in Gray-Scott justifies (decorative).
5. The Scream: overstated claim that transient length is formally unpredictable/unbounded.

**Should fix (framing/accuracy):**
6. Great Wave complexity: replace Navier-Stokes centrepiece with the Courant stability condition (true of this algorithm).
7. Great Wave table: replace decorative columns with a space-vs-time Courant trade-off table.
8. Great Wave real-world: tsunami models use shallow-water equations, not the plain wave equation.
9. The Scream table: replace with a bespoke table reflecting its actual cost story.

**Leave alone (verified correct):**
- Gray-Scott equations as written.
- Starry Night O(n) treatment and its O(n²) column (motivated by inter-particle forces / Tier 4).
- Courant condition c·Δt/Δx ≤ 1/√2 for 2D wave equation.
- 2012 mouse-digit Turing confirmation (Sheth et al., Science).
- Clay Institute seven problems designated 2000.

---

## Part 2 — Great Wave: corrected copy

### B — The algorithm (heading unchanged)

**Body — replace with:**

Hokusai's wave captures the moment before a crest breaks. We don't reproduce the physics of a breaking wave — that's far harder than it looks. Instead we simulate the *wave equation*: the rule that governs how a disturbance travels through a medium at a fixed speed *c*. It's the same equation behind sound in air, light in a vacuum, and the vibration of a drum skin. It is not the equation that governs real water — more on that below — but it produces the travelling, interfering ripples that give the piece its motion.

Each point on the grid stores a height. Its next height depends on its current height, its height one step ago, and the heights of its four nearest neighbours. There's no matrix to invert and no global system to solve: every cell updates from local information alone. The wave emerges from the aggregate of these local interactions.

**Eq. 1 (unchanged):**

∂²η/∂t² = c²∇²η

*Eq. 1 — 2D wave equation (height η, wave speed c)*

**Eq. 2 — corrected:**

η_{t+1} = 2η_t − η_{t−1} + (c²Δt² / Δx²) ∇²η_t

*Eq. 2 — explicit finite-difference update. ∇²η_t is the discrete Laplacian: the sum of the four neighbours minus four times the centre cell.*

**Code block — unchanged, but add this comment near the top of the loop:**

```
# Note: we work in grid units, so dx = 1 and the dx**2 term from the
# textbook equation disappears here. c is therefore in cells-per-step,
# not metres-per-second.
```

---

### C — The complexity

**Heading — replace with:**

### Linear in space — but you can't take any timestep you like

**Body — replace entire section with:**

The update rule is O(n) per time step, where *n* is the number of grid cells. Each cell reads its four neighbours and applies a fixed formula, so doubling the grid doubles the work. No surprises in the *space* cost.

The interesting cost is hidden in *time*. This is an explicit solver: it computes the next state purely from states it already has. Explicit solvers are cheap per step, but they are not free — they are only stable if the timestep is small enough. Push the wave speed *c* or the timestep Δt too high and the simulation doesn't just get inaccurate, it detonates: heights race off to infinity within a few frames.

The boundary is the *Courant–Friedrichs–Lewy condition*. For the 2D wave equation it is:

c · Δt / Δx ≤ 1/√2

Intuitively: information in the real wave travels at speed *c*. In one timestep it should not cross more than one grid cell. If your scheme lets a disturbance jump further per step than the physics allows, the solver loses track of cause and effect, and the errors compound geometrically. The 1/√2 is the two-dimensional correction — a disturbance can travel diagonally, and the diagonal is longer than the side.

You can feel this trade-off directly. Halving Δx for a sharper wave forces you to at least halve Δt to stay stable, which means twice as many steps to cover the same span of time. Finer space costs you more in time than the O(n) grid count alone suggests.

**Table — replace the decorative three-column table with:**

| grid resolution | cells n (O(n) space) | max stable Δt | steps for 1 sim-second |
| --------------- | -------------------- | ------------- | ---------------------- |
| 100 × 100       | 10,000               | Δt₀           | T                      |
| 200 × 200       | 40,000               | Δt₀ / 2       | 2T                     |
| 400 × 400       | 160,000              | Δt₀ / 4       | 4T                     |
| 800 × 800       | 640,000              | Δt₀ / 8       | 8T                     |

*Caption:* Doubling the linear resolution multiplies the cell count by 4 and forces the timestep down by 2. The total work to simulate a fixed duration therefore scales as roughly the **cube** of the linear resolution, not the square. The Courant condition is why high-resolution wave and seismic models are so expensive: the cost is in the timesteps as much as the cells.

**Add this digression box (clearly styled as an aside, not the main thread):**

> **Why not simulate real water?**
> Real water is governed by the Navier–Stokes equations: non-linear, fully coupled, and genuinely unsolved — whether smooth 3D solutions always exist is one of the Clay Mathematics Institute's seven Millennium Prize Problems, worth $1,000,000 and open since 2000. The wave equation we used here is not a simplified Navier–Stokes; it's a different equation entirely, linear where Navier–Stokes is non-linear. We didn't approximate the hard problem — we sidestepped it by solving an easier one that happens to look convincing. Most real-time water you've seen in games does the same.

---

### D — In the real world

**Tsunami entry — replace with:**

**Tsunami prediction.** NOAA's DART buoy network detects pressure changes on the deep-ocean floor; propagation models then project arrival times and wave heights. Those models use the shallow-water equations — a relative of the wave equation that shares its travelling-disturbance behaviour but adds terms the linear version omits. The 2004 Indian Ocean tsunami exposed how few such systems existed at the time and drove their expansion across the Pacific and Indian Oceans.

**Aeroacoustics and seismology entries — unchanged (genuinely wave-equation problems).**

**Closing question — replace with:**

*Your simulation is 2D, linear, and never lets a wave break. A real ocean wave is none of those things. Of the three — adding a third dimension, adding non-linearity, or allowing the wave to break — which do you think costs the most to simulate, and which matters most for predicting where a tsunami makes landfall? They might not be the same answer.*

---

## Part 3 — The Scream: corrected copy

### B — The algorithm

**No factual errors in the equations or mechanism description. One small precision fix:**

The line "better known for his work on computation and codebreaking" is fine. The mechanism description (U fed at F, autocatalytic UV², V decays, differential diffusion) is correct. Leave section B as-is except for one optional clarity addition: state explicitly that F and k are the feed and kill rates already named in the simulation controls, so the link between the sliders and the equations is unambiguous.

---

### C — The complexity

**Heading — replace with:**

### Linear per step — but the step count is the real cost, and it's hard to bound

**Body — replace entire section with:**

Like the others, the update is O(n) per step: each cell reads its four neighbours and applies a fixed formula. The space cost holds no surprises. The cost that matters here is the *number of steps* — and that's where Gray-Scott gets genuinely awkward.

The system has a transient phase: a stretch of apparent disorder before a coherent pattern settles. For most parameter choices that transient is finite but its length varies enormously, and there's no simple formula that takes (F, k) and the initial conditions and returns "it will settle after this many steps." In practice you find out by running it. For some parameter regimes the system never settles at all — it stays in perpetual motion, spots endlessly splitting and dying.

This isn't just a Gray-Scott quirk. Reaction–diffusion systems in general are computationally powerful: researchers have shown that suitably configured reaction–diffusion media can perform computation — building logic gates and, in principle, universal computers out of travelling chemical waves. The moment a system can simulate a general computer, asking "will this configuration ever reach a stable state?" becomes a version of the *halting problem*: in the general case, undecidable. There is no algorithm that takes any program and tells you whether it eventually stops; for a sufficiently expressive reaction–diffusion system, the same wall applies to "will this pattern ever settle?"

That's the honest shape of the complexity story here. The per-step arithmetic is trivial. The hard part — how long, or whether ever — is not something you can shortcut by being clever, and at the extreme it's not something any algorithm can answer in general.

**Table — replace the decorative table with a "cost lives in the step count" framing:**

| what you're measuring | cost | can you predict it in advance? |
| --------------------- | ---- | ------------------------------ |
| one update step       | O(n), n = grid cells | yes — fixed work per cell |
| steps until pattern settles | varies wildly with (F, k) | no general formula; run it to find out |
| whether it settles at all | — | undecidable in the general case for computationally universal reaction–diffusion systems |

*Caption:* The same O(n) per-step cost as the other two paintings — but here the open question isn't "how big is n," it's "how many steps, and will it ever stop?" That second question is, in full generality, beyond what any algorithm can answer.

**Precision note on the "undecidable" claim (important — do not overstate):**

The undecidability result applies to reaction–diffusion systems *in general* — the class is computationally universal, so the halting-style question is undecidable for the class. It is NOT a proven theorem that the *specific* Gray-Scott model with its standard parameter range is itself Turing-complete or that its convergence is formally undecidable. The copy above is careful to say "reaction–diffusion systems in general" and "for a sufficiently expressive reaction–diffusion system," not "Gray-Scott is undecidable." Keep that distinction. Overstating it would be exactly the kind of error we just fixed in the Great Wave section.

---

### D — In the real world (unchanged — all three entries verified correct)

---

## Part 4 — Starry Night

No corrections required. The O(n) treatment is sound and the O(n²) column is legitimately motivated by the inter-particle-force scenario in Tier 4. One optional improvement: the underspecified "curl of a scalar noise function" could name the streamfunction convention (velocity = (∂ψ/∂y, −∂ψ/∂x)) so a precise reader isn't left wondering what "curl of a scalar" means in 2D. Optional, not a factual error.

---

## Part 5 — Cross-site consistency note

After these fixes, the three complexity sections will each tell a *different and true* story, which is the point:

- **Starry Night:** linear and embarrassingly parallel — the baseline. O(n²) only if you add interaction (Tier 4).
- **Great Wave:** linear in space, but the Courant condition couples space and time — finer grids cost cubically.
- **The Scream:** linear per step, but the step count is unbounded-in-practice and undecidable-in-general.

That progression — trivially parallel → constrained by stability → bounded by computability itself — is a genuinely strong arc for an A-level audience, and it earns the P vs NP / undecidability material honestly rather than bolting it on.

---

# Part 6 — Prompt for Claude Code

Copy everything below the line into Claude Code.

---

You are editing an existing live project, Deep Patterns, an A-level Computer Science enrichment site. The repository is `djh-kings/Deep-Patterns`, deployed via GitHub Pages from `main`. The site is a single-page HTML/JS application with three painting sections (Starry Night, Great Wave, The Scream), each with sub-sections A (simulation), B (algorithm), C (complexity), D (real world).

I have a corrections document with verified, factually-checked replacement copy for two of the three sections. Your job is to apply these edits precisely to the existing page without altering anything not specified, and without breaking the existing simulations, styling, scroll-reveal animations, or layout.

## Constraints

- Do NOT change the visual design, the colour scheme, the typography, the scroll-snap navigation, or the complexity-table reveal animation mechanism. You are editing text content and one set of table rows, nothing else.
- Do NOT touch the Starry Night section except for one optional clarification (see below) — confirm with me before making even that change.
- Preserve all existing IDs, anchor links, and class names so navigation and animations keep working.
- The complexity tables are animated on scroll (rows reveal, then numbers count up). When you replace a table's contents, the new table must use the same markup pattern and classes as the existing ones so the reveal animation still fires. If the number-counting animation assumes purely numeric cells, flag any new non-numeric cells (e.g. "undecidable", "Δt₀/2") that might break it, and propose how to handle them rather than silently breaking the animation.
- House code style for any Python you touch is camelCase (non-standard but required). The site's downloadable scripts are separate; do not edit them in this task unless I ask.
- UK English throughout.

## Edits to make

### Great Wave — Section B (algorithm)
1. Replace the body paragraph(s) with the corrected text in Part 2 of the corrections doc. Core change: this is the linear *wave equation*, explicitly NOT fluid dynamics and NOT a simplified Navier-Stokes.
2. Replace displayed Equation 2 with the corrected version including the (c²Δt²/Δx²) coefficient and a correct discrete-Laplacian description. The old one had a typo (`∇2h`) and a missing Δx² term.
3. Remove the false statement "Each cell is independent." Use the corrected wording (cells update from local neighbour information).
4. Add the specified explanatory comment to the displayed code block about dx = 1 / grid units.

### Great Wave — Section C (complexity)
5. Replace the heading with: "Linear in space — but you can't take any timestep you like".
6. Replace the entire body with the Courant-condition treatment in Part 2. This removes the Navier-Stokes-as-centrepiece framing.
7. Replace the complexity table with the four-row space-vs-time Courant table (resolution / cells / max stable Δt / steps for 1 sim-second). Note: cells contain symbolic values like "Δt₀/2" and "2T", not plain integers — handle the count-up animation accordingly (see constraints).
8. Add the "Why not simulate real water?" digression box as a visually distinct aside (not a main paragraph). It should read as a sidebar, styled differently from body text. This is where the Navier-Stokes Millennium Prize content now lives, honestly framed.

### Great Wave — Section D (real world)
9. Replace the tsunami paragraph with the corrected shallow-water-equations version.
10. Leave aeroacoustics and seismology unchanged.
11. Replace the closing italic question with the corrected 2D/non-linear/breaking version.

### The Scream — Section B (algorithm)
12. Optional small addition only: state that F and k in the equations are the same feed and kill rates as the simulation sliders. No other changes to B.

### The Scream — Section C (complexity)
13. Replace the heading with: "Linear per step — but the step count is the real cost, and it's hard to bound".
14. Replace the entire body with the transient/undecidability treatment in Part 3. CRITICAL: the copy is deliberately careful to say undecidability applies to reaction–diffusion systems *in general*, NOT that Gray-Scott specifically is proven undecidable. Do not "tighten" or paraphrase this in a way that strengthens the claim — the precise hedging is intentional and factually load-bearing.
15. Replace the complexity table with the three-row "what you're measuring / cost / can you predict it" table. This table is mostly non-numeric — it should NOT use the number-count-up animation. Use the row-reveal animation only, or static display if row-reveal assumes numeric cells. Flag what you chose.

### Starry Night
16. No required changes. Optionally, in Section B, name the streamfunction convention (velocity = (∂ψ/∂y, −∂ψ/∂x)) to clarify what "curl of a scalar function" means in 2D. Ask me before doing this.

## After editing

- Give me a short diff summary: which paragraphs, equations, and tables changed in each section.
- Confirm the three complexity tables now differ from one another (they were previously identical) and that each one's reveal animation still works.
- Flag anything in my corrected copy that you think is still wrong, ambiguous, or that breaks when rendered. Push back if you spot an error — I would rather hear it now.
- Do not deploy or push. Show me the changes first. I will review and merge.

