"""
Deep Patterns — Starry Night
Curl-noise particle flow field

Algorithm: Curl noise derived from a scalar potential field ψ(x,y,t).
The curl of a 2D scalar gives a divergence-free velocity field:
    vx =  ∂ψ/∂y
    vy = -∂ψ/∂x

Complexity: O(n) per frame where n = number of particles.

Dependencies: numpy, matplotlib
Install:  pip install numpy matplotlib
Run:      python starry_night.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# ── Parameters (edit these) ───────────────────────────────────────────────────
N_PARTICLES   = 2000       # number of flow particles
PARTICLE_LIFE = 120        # frames before a particle resets
FIELD_SCALE   = 0.012      # spatial frequency of the potential field
SPEED         = 1.8        # particle speed multiplier
ALPHA_DECAY   = 0.96       # trail fade per frame (lower = shorter trails)
WIDTH, HEIGHT = 800, 600   # canvas size in pixels
FPS           = 30         # target frame rate
# ─────────────────────────────────────────────────────────────────────────────

rng = np.random.default_rng(42)


def psi(x: np.ndarray, y: np.ndarray, t: float) -> np.ndarray:
    """Scalar potential field — superposition of sinusoidal basis functions."""
    z = FIELD_SCALE
    return (  np.sin(x * z * 1.8 + t) * np.cos(y * z * 2.2 + t * 0.7)
            + np.sin(x * z * 2.6 - t * 0.5) * np.cos(y * z * 2.0 + t * 0.8)
            + np.sin((x + y) * z * 1.5 + t * 0.6) * 0.5 )


def curl(x: np.ndarray, y: np.ndarray, t: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Numerical curl via central finite differences.
    Returns (vx, vy) = (∂ψ/∂y, -∂ψ/∂x).
    The result is exactly divergence-free: ∂vx/∂x + ∂vy/∂y = 0.
    """
    eps = 1.0
    dpdy = (psi(x, y + eps, t) - psi(x, y - eps, t)) / (2 * eps)
    dpdx = (psi(x + eps, y, t) - psi(x - eps, y, t)) / (2 * eps)
    return dpdy * SPEED * 55, -dpdx * SPEED * 55


class CurlFlowField:
    def __init__(self):
        self.t = 0.0
        # Particle positions
        self.px = rng.uniform(0, WIDTH,  N_PARTICLES)
        self.py = rng.uniform(0, HEIGHT, N_PARTICLES)
        # Age in frames (staggered so particles don't all reset together)
        self.age = rng.integers(0, PARTICLE_LIFE, N_PARTICLES)
        # Per-particle hue offset for Van Gogh's yellow-blue palette
        self.hue_offset = rng.uniform(0, 1, N_PARTICLES)

    def reset_particles(self, mask: np.ndarray):
        n = mask.sum()
        self.px[mask] = rng.uniform(0, WIDTH,  n)
        self.py[mask] = rng.uniform(0, HEIGHT, n)
        self.age[mask] = 0

    def step(self):
        vx, vy = curl(self.px, self.py, self.t * 0.0005)
        self.px += vx * (1 / FPS)
        self.py += vy * (1 / FPS)
        self.age += 1

        # Reset particles that leave the canvas or exceed lifespan
        oob = ((self.px < 0) | (self.px >= WIDTH) |
               (self.py < 0) | (self.py >= HEIGHT) |
               (self.age >= PARTICLE_LIFE))
        if oob.any():
            self.reset_particles(oob)

        self.t += 1

    def get_points(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return (x, y, alpha) arrays for current particle positions."""
        alpha = (self.age / PARTICLE_LIFE).clip(0, 1)
        return self.px, self.py, alpha


def build_colormap():
    """Van Gogh deep-blue to cadmium-yellow palette."""
    colors = [
        (0.04, 0.06, 0.15),   # near-black blue
        (0.04, 0.16, 0.45),   # deep Prussian blue
        (0.18, 0.38, 0.70),   # mid cornflower
        (0.90, 0.78, 0.10),   # cadmium yellow
        (0.98, 0.92, 0.55),   # pale gold
    ]
    return LinearSegmentedColormap.from_list("starry_night", colors, N=256)


def main():
    sim = CurlFlowField()
    cmap = build_colormap()

    fig, ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100)
    fig.patch.set_facecolor("#0d0d14")
    ax.set_facecolor("#0a0a11")
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0)

    # Use scatter for particles; colour by normalised y position
    sc = ax.scatter(sim.px, sim.py, s=1.2, c=sim.py / HEIGHT,
                    cmap=cmap, alpha=0.0, linewidths=0)

    title = ax.set_title(
        "Curl-noise flow field  ·  N = {:,} particles  ·  O(n) per frame".format(N_PARTICLES),
        color="#aaaaaa", fontsize=9, pad=6,
    )

    def update(frame):
        sim.step()
        x, y, alpha = sim.get_points()

        sc.set_offsets(np.column_stack([x, y]))
        sc.set_array(y / HEIGHT)
        # Map per-particle alpha through a masked array approach:
        # We vary sizes slightly with alpha for a fading-trail feel.
        sc.set_sizes(alpha * 2.5)
        sc.set_alpha(None)           # let per-point sizes carry the fade
        title.set_text(
            "Curl-noise flow  ·  t = {:,}  ·  N = {:,} particles  ·  O(n)".format(
                sim.t, N_PARTICLES)
        )
        return sc, title

    ani = animation.FuncAnimation(
        fig, update, interval=1000 // FPS, blit=True, cache_frame_data=False
    )

    plt.show()


if __name__ == "__main__":
    main()
