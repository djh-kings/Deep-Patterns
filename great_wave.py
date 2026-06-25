"""
Deep Patterns — The Great Wave
2D wave equation via explicit finite-difference Verlet integration

Equation:   ∂²η/∂t² = c² ∇²η
Scheme:     η[t+1] = 2η[t] - η[t-1] + c²·Δt²·∇²η[t]
Stability:  Courant condition  c·Δt/Δx ≤ 1/√2  (satisfied here with c ≤ 0.49)

Complexity: O(n) per timestep, where n = grid cells = W × H.

Dependencies: numpy, matplotlib
Install:  pip install numpy matplotlib
Run:      python great_wave.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# ── Parameters (edit these) ───────────────────────────────────────────────────
W, H       = 200, 140    # grid dimensions (cells)
C          = 0.45        # wave speed (Courant number per cell per step)
DAMPING    = 0.9995      # energy loss per step (1.0 = lossless)
STEPS_PER_FRAME = 4      # simulation steps per animation frame
SOURCE_X   = W // 4     # initial wave source x position
SOURCE_Y   = H // 2     # initial wave source y position
FPS        = 30          # target frame rate
# ─────────────────────────────────────────────────────────────────────────────

rng = np.random.default_rng(0)


class WaveSimulation:
    def __init__(self):
        self.prev = np.zeros((H, W), dtype=np.float32)
        self.curr = np.zeros((H, W), dtype=np.float32)
        self.next = np.zeros((H, W), dtype=np.float32)
        self.t = 0

        # Seed with a Gaussian pulse at the source position
        y_idx, x_idx = np.mgrid[0:H, 0:W]
        dist2 = (x_idx - SOURCE_X)**2 + (y_idx - SOURCE_Y)**2
        self.curr[:] = np.exp(-dist2 / 60.0).astype(np.float32)
        self.prev[:] = self.curr * 0.98   # slight asymmetry to start propagation

    def step(self):
        """One Verlet step of the explicit finite-difference scheme."""
        c2 = C ** 2

        # 5-point Laplacian with Dirichlet (zero) boundary conditions
        lap = (
            np.roll(self.curr,  1, axis=1) +
            np.roll(self.curr, -1, axis=1) +
            np.roll(self.curr,  1, axis=0) +
            np.roll(self.curr, -1, axis=0) -
            4 * self.curr
        )

        # Verlet update
        self.next = (2 * self.curr - self.prev + c2 * lap) * DAMPING

        # Absorbing boundary: zero out edges to prevent wrap-around reflections
        self.next[[0, -1], :] = 0
        self.next[:, [0, -1]] = 0

        # Rotate buffers (no allocation)
        self.prev, self.curr, self.next = self.curr, self.next, self.prev
        self.t += 1

    def add_source(self, gx: int, gy: int, amplitude: float = 1.5):
        """Add a point disturbance at grid coordinates (gx, gy)."""
        gy = int(np.clip(gy, 1, H - 2))
        gx = int(np.clip(gx, 1, W - 2))
        self.curr[gy-1:gy+2, gx-1:gx+2] += amplitude

    def add_barrier(self, gx: int):
        """Add a vertical barrier at column gx (reflection obstacle)."""
        col = int(np.clip(gx, 1, W - 2))
        self.curr[:, col] = 0
        self.prev[:, col] = 0


def build_colormap():
    """Hokusai ocean palette: deep indigo through Prussian blue to white foam."""
    colors = [
        (0.02, 0.06, 0.22),   # deep indigo
        (0.05, 0.15, 0.40),   # Prussian blue
        (0.10, 0.28, 0.60),   # cobalt
        (0.20, 0.50, 0.80),   # cerulean
        (0.70, 0.85, 0.96),   # pale sky
        (0.97, 0.98, 1.00),   # foam white
    ]
    return LinearSegmentedColormap.from_list("great_wave", colors, N=256)


def main():
    sim = WaveSimulation()
    cmap = build_colormap()
    cmap.set_under("#010614")

    fig, ax = plt.subplots(figsize=(10, 7), dpi=100)
    fig.patch.set_facecolor("#0d0d14")
    ax.set_facecolor("#010614")
    ax.axis("off")
    fig.tight_layout(pad=0)

    img = ax.imshow(
        sim.curr, cmap=cmap, vmin=-0.6, vmax=0.6,
        origin="lower", interpolation="bicubic",
        aspect="auto", extent=[0, W, 0, H],
    )

    title = ax.set_title(
        "2D Wave equation  ·  {}×{} grid  ·  c = {}  ·  O(n) per step".format(W, H, C),
        color="#aaaaaa", fontsize=9, pad=6,
    )

    info = ax.text(
        0.02, 0.96, "Click to add wave source  ·  Shift+click to add barrier",
        transform=ax.transAxes, color="#555566", fontsize=8,
        va="top", fontfamily="monospace",
    )

    def update(frame):
        for _ in range(STEPS_PER_FRAME):
            sim.step()
        img.set_data(sim.curr)
        title.set_text(
            "Wave equation  ·  t = {:,}  ·  {}×{} grid  ·  O(n)".format(sim.t, W, H)
        )
        return img, title

    def on_click(event):
        if event.inaxes is not ax:
            return
        gx = int(np.clip(event.xdata, 1, W - 2))
        gy = int(np.clip(event.ydata, 1, H - 2))
        if event.key == "shift":
            sim.add_barrier(gx)
        else:
            sim.add_source(gx, gy, amplitude=1.8)

    fig.canvas.mpl_connect("button_press_event", on_click)

    ani = animation.FuncAnimation(
        fig, update, interval=1000 // FPS, blit=True, cache_frame_data=False
    )

    print("Controls:")
    print("  Click            — add wave source at cursor position")
    print("  Shift + Click    — add vertical reflective barrier")
    print("  Close window     — quit")

    plt.show()


if __name__ == "__main__":
    main()
