"""
Deep Patterns — The Scream
Gray-Scott reaction-diffusion system (Turing morphogenesis)

Equations:
    ∂u/∂t = Du·∇²u  −  u·v²  +  F·(1 − u)
    ∂v/∂t = Dv·∇²v  +  u·v²  −  (F + k)·v

Species u (activator) and v (inhibitor) diffuse and react to produce
spontaneous spatial patterning — spots, stripes, or labyrinths depending
on feed rate F and kill rate k.

Complexity: O(n) per step, where n = grid cells = W × H.

Dependencies: numpy, matplotlib
Install:  pip install numpy matplotlib
Run:      python the_scream.py

Parameter presets at the bottom of this file let you switch between
pattern modes (spots, stripes, worms, Turing rings, coral).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# ── Pattern presets — uncomment one ──────────────────────────────────────────
# Each preset is (F, k, Du) — these produce qualitatively different patterns.

PRESET = "mitosis"    # name for display

PRESETS = {
    "mitosis":     (0.0367, 0.0649, 0.19),   # self-replicating spots
    "coral":       (0.0545, 0.062,  0.18),   # coral / dendritic growth
    "stripes":     (0.022,  0.051,  0.14),   # parallel stripe Turing patterns
    "worms":       (0.078,  0.061,  0.16),   # worm-like labyrinthine trails
    "fingerprint": (0.037,  0.060,  0.20),   # fingerprint ridges
}

F0, K0, DU0 = PRESETS[PRESET]

# ── Parameters (edit these) ──────────────────────────────────────────────────
W, H              = 200, 200     # grid dimensions
F                 = F0           # feed rate
K                 = K0           # kill rate
DU                = DU0          # diffusion coefficient for u
DV                = DU / 2       # diffusion coefficient for v (always DU/2)
STEPS_PER_FRAME   = 12           # steps per animation frame
FPS               = 30           # target frame rate
SEED_RADIUS       = 8            # radius of initial perturbation seeds
N_SEEDS           = 6            # number of initial seeds
# ─────────────────────────────────────────────────────────────────────────────

rng = np.random.default_rng(7)


class GrayScott:
    def __init__(self):
        self.u = np.ones((H, W), dtype=np.float32)
        self.v = np.zeros((H, W), dtype=np.float32)
        self.t = 0
        self._seed()

    def _seed(self):
        """Place small square perturbations of v to seed pattern formation."""
        for _ in range(N_SEEDS):
            cx = rng.integers(SEED_RADIUS, W - SEED_RADIUS)
            cy = rng.integers(SEED_RADIUS, H - SEED_RADIUS)
            r = SEED_RADIUS
            self.v[cy-r:cy+r, cx-r:cx+r] = 0.25 + rng.uniform(-0.01, 0.01, (2*r, 2*r))
            self.u[cy-r:cy+r, cx-r:cx+r] = 0.50 + rng.uniform(-0.01, 0.01, (2*r, 2*r))

    def laplacian(self, grid: np.ndarray) -> np.ndarray:
        """5-point Laplacian with periodic (wrap-around) boundary conditions."""
        return (
            np.roll(grid,  1, axis=1) +
            np.roll(grid, -1, axis=1) +
            np.roll(grid,  1, axis=0) +
            np.roll(grid, -1, axis=0) -
            4 * grid
        )

    def step(self):
        """One Gray-Scott update step (Euler integration, dt = 1)."""
        uvv = self.u * self.v * self.v

        lu = self.laplacian(self.u)
        lv = self.laplacian(self.v)

        self.u += DU * lu - uvv + F * (1 - self.u)
        self.v += DV * lv + uvv - (F + K) * self.v

        np.clip(self.u, 0, 1, out=self.u)
        np.clip(self.v, 0, 1, out=self.v)
        self.t += 1

    def add_seed(self, gx: int, gy: int):
        """Inject a small perturbation at (gx, gy) in grid coordinates."""
        r = SEED_RADIUS
        gy = int(np.clip(gy, r, H - r - 1))
        gx = int(np.clip(gx, r, W - r - 1))
        self.v[gy-r:gy+r, gx-r:gx+r] = 0.25
        self.u[gy-r:gy+r, gx-r:gx+r] = 0.50


def build_colormap():
    """Munch blood-orange and tormented sky palette."""
    colors = [
        (0.05, 0.02, 0.03),   # near-black
        (0.30, 0.08, 0.04),   # dark blood
        (0.72, 0.20, 0.07),   # blood orange
        (0.91, 0.38, 0.12),   # Munch orange
        (0.97, 0.72, 0.30),   # amber
        (0.99, 0.96, 0.80),   # pale cream
    ]
    return LinearSegmentedColormap.from_list("the_scream", colors, N=256)


def main():
    sim = GrayScott()
    cmap = build_colormap()

    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    fig.patch.set_facecolor("#0d0d14")
    ax.set_facecolor("#0d0407")
    ax.axis("off")
    fig.tight_layout(pad=0)

    img = ax.imshow(
        sim.v, cmap=cmap, vmin=0, vmax=0.35,
        origin="lower", interpolation="nearest",
        aspect="equal", extent=[0, W, 0, H],
    )

    title = ax.set_title(
        "Gray-Scott  ·  preset: {}  ·  F={:.4f}  k={:.4f}  ·  {}×{}".format(
            PRESET, F, K, W, H),
        color="#aaaaaa", fontsize=9, pad=6,
    )

    info = ax.text(
        0.02, 0.97,
        "Click to seed new pattern  ·  showing species v",
        transform=ax.transAxes, color="#554433", fontsize=8,
        va="top", fontfamily="monospace",
    )

    def update(frame):
        for _ in range(STEPS_PER_FRAME):
            sim.step()
        img.set_data(sim.v)
        title.set_text(
            "Gray-Scott  ·  preset: {}  ·  t = {:,}  ·  O(n)".format(PRESET, sim.t)
        )
        return img, title

    def on_click(event):
        if event.inaxes is not ax:
            return
        gx = int(np.clip(event.xdata, 0, W - 1))
        gy = int(np.clip(event.ydata, 0, H - 1))
        sim.add_seed(gx, gy)

    fig.canvas.mpl_connect("button_press_event", on_click)

    ani = animation.FuncAnimation(
        fig, update, interval=1000 // FPS, blit=True, cache_frame_data=False
    )

    print("Gray-Scott reaction-diffusion — Deep Patterns")
    print("  Preset:   {} (F={}, k={}, Du={})".format(PRESET, F, K, DU))
    print()
    print("  Other presets (edit PRESET at the top of the file):")
    for name, (f, k, du) in PRESETS.items():
        marker = " ←" if name == PRESET else ""
        print("    {:12s}  F={:.4f}  k={:.4f}  Du={}{}".format(name, f, k, du, marker))
    print()
    print("  Click in the window to seed new patterns.")

    plt.show()


if __name__ == "__main__":
    main()
