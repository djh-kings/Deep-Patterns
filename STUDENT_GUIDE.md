# Deep Patterns — Student Guide

Welcome. This guide tells you how to explore the three simulations and what to
look for. You don't need to be able to code to use it — but by the end, the goal
is that you could *build* one of these yourself.

Take your time. This isn't meant to be finished in one sitting.

---

## What is this?

Three famous paintings, three algorithms. Each painting has a visual quality —
swirling skies, a breaking wave, a turbulent scream — that a computer can
reproduce with a surprisingly short piece of code. For each one you get:

- **A** — a live simulation you can play with,
- **B** — the algorithm behind it, with the actual equations,
- **C** — how the cost grows as you make it bigger (its *complexity*),
- **D** — where the same idea turns up in the real world.

The three are independent — start with whichever painting appeals to you most.

---

## Using the website

Open the page and scroll. Each painting has a control panel on the left (the
simulation and its sliders) and the explanation on the right.

### Controls that appear on every simulation

- **Sliders** — drag to change a parameter. The value updates live as you drag,
  and the simulation responds immediately. Change one thing at a time so you can
  see what it does.
- **Run** — starts the animation if it's paused.
- **Reset (↺)** — clears everything back to the starting state. Use this whenever
  a simulation gets messy and you want a clean slate.
- **Replay reveal (↻)** on the tables — re-plays the little counting animation on
  the complexity table.

### 🌌 The Starry Night — flow field

Thousands of tiny particles drift along invisible "currents" and trace out
Van Gogh's swirling brushstrokes.

- **Drag your mouse across the canvas** to pull the flow around.
- **Sliders:** *Particles* (how many dots), *Field scale* (how tight the swirls
  are), *Flow speed* (how fast they move).
- **Try this:** turn the particle count right down, watch a few individual dots,
  and see that each one just follows the current near it — no dot pays any
  attention to the others. That simple fact is the whole reason it's fast.

### 🌊 The Great Wave — wave equation

A grid of water heights ripples and interferes like the surface of a pond.

- **Click** anywhere to drop a new wave source and watch the ripples spread and
  bounce.
- **Sliders:** *Wave speed*, *Damping* (how quickly waves fade), *Source
  amplitude* (how big a splash each click makes).
- **Try this:** push the *Wave speed* slider high and watch it eventually break
  down into noise. There's a real limit (the *Courant condition*) beyond which the
  method becomes unstable — the panel explains it. Physics has speed limits, and
  so does the maths that simulates it.

### 🎭 The Scream — reaction–diffusion

Two imaginary chemicals spread and react, growing spots and stripes out of almost
nothing — the mechanism Alan Turing proposed in 1952 for how animals get their
markings.

- **Click on the dark areas** to seed a new patch. Watch it grow and *divide* —
  this default setting is nicknamed "mitosis" because it behaves like cells
  splitting.
- **Sliders:** *Feed rate*, *Kill rate*, *Diffusion ratio*. These are sensitive —
  small changes give completely different patterns (spots, worms, coral). Nudge
  them gently.
- **Try this:** change the feed/kill sliders a little, hit Reset, and see how
  different the pattern becomes. Then try to find settings that make stripes
  instead of spots.

---

## What to actually look for

The paintings are the hook; the ideas are the point. As you play, keep these
questions in mind — they're what the panels are really about:

1. **Why is it fast?** All three do the *same amount of work per element* each
   step (`O(n)` — "order n"). Double the size, double the work. The tables show
   how much worse life gets if that were `O(n²)` instead.
2. **What did we leave out?** These are *simplified* models. The Great Wave uses
   the linear wave equation, **not** the full physics of real, breaking water
   (that's a famously unsolved problem — see the $1,000,000 Millennium Prize
   callout). Knowing what a model ignores is as important as knowing what it does.
3. **Where is this used for real?** Weather, tsunami warnings, brain imaging,
   animal-marking biology, VFX — the same loops you're clicking on, scaled up.

---

## Want to go further? Run the code

Every simulation on the page also exists as a short, commented Python program you
can read and change: `starry_night.py`, `great_wave.py`, `the_scream.py`.

You'll need Python with two common libraries:

```bash
pip install numpy matplotlib
python starry_night.py
```

Open the file in an editor first — the adjustable settings are in a clearly
labelled block at the top, and each file prints its controls when it starts.
Change a number, run it again, see what happens. That loop — *change something,
predict, check* — is the entire job.

---

## The challenge

Down in the **Downloads** section of the site there are tiered challenges for each
painting, from *observe* up to *rebuild it yourself*. Pick one painting and see
how far up the tiers you can climb. There's no deadline and no single right
answer — that's the point.

Have fun. Break things. Hit Reset. Ask why.
