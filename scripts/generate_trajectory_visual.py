"""
Generate a polished trajectory + decision visualization for the README.

This script simulates a vehicle navigating an urban route using the kinematic
bicycle model, overlaying Alpamayo R1-style decisions at each waypoint.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import os

def kinematic_bicycle_step(x, y, theta, v, delta, L, dt):
    """Kinematic bicycle model (mirrors the Julia implementation)."""
    dx = v * np.cos(theta)
    dy = v * np.sin(theta)
    dtheta = (v / L) * np.tan(delta)
    return x + dx * dt, y + dy * dt, theta + dtheta * dt

def generate_trajectory():
    """Simulate a realistic urban driving trajectory with varying decisions."""
    L = 2.7  # wheelbase (m)
    dt = 0.1
    
    # Waypoints with (steering_sequence, speed, frames, decision, confidence)
    segments = [
        # Accelerate out of parking
        (0.0, 8.0, 40, "accelerate", 0.92),
        # Slight right curve
        (0.08, 12.0, 50, "maintain_speed", 0.95),
        # Approach intersection — slow down
        (0.02, 6.0, 30, "slow_down", 0.88),
        # Stop at red light
        (0.0, 0.5, 15, "stop", 0.97),
        # Green light — accelerate through
        (0.0, 10.0, 35, "accelerate", 0.91),
        # Sharp left turn
        (-0.15, 7.0, 45, "slow_down", 0.85),
        # Yield to pedestrian
        (-0.02, 3.0, 20, "yield", 0.93),
        # Resume speed on straight
        (0.01, 14.0, 60, "accelerate", 0.90),
        # Gentle right curve
        (0.06, 12.0, 50, "maintain_speed", 0.94),
        # Brake for obstacle
        (0.0, 2.0, 15, "brake", 0.96),
        # Final coast
        (0.02, 10.0, 40, "maintain_speed", 0.89),
    ]
    
    xs, ys, speeds, decisions, confidences = [], [], [], [], []
    x, y, theta = 0.0, 0.0, np.pi / 6  # start heading NE
    
    for steer, speed, frames, decision, conf in segments:
        for i in range(frames):
            xs.append(x)
            ys.append(y)
            speeds.append(speed)
            decisions.append(decision)
            confidences.append(conf)
            x, y, theta = kinematic_bicycle_step(x, y, theta, speed, steer, L, dt)
    
    return np.array(xs), np.array(ys), np.array(speeds), decisions, confidences

def plot_trajectory(xs, ys, speeds, decisions, confidences):
    """Create the publication-quality visualization."""
    
    # Color map for decisions
    decision_colors = {
        "accelerate": "#22c55e",
        "maintain_speed": "#3b82f6",
        "slow_down": "#f59e0b",
        "stop": "#ef4444",
        "yield": "#a855f7",
        "brake": "#dc2626",
    }
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor="#0f172a")
    ax.set_facecolor("#0f172a")
    
    # --- Colored trajectory line segments ---
    points = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    colors = [decision_colors.get(d, "#888") for d in decisions[:-1]]
    lc = LineCollection(segments, colors=colors, linewidths=3, alpha=0.85)
    ax.add_collection(lc)
    
    # --- Decision change markers ---
    prev_decision = None
    marker_xs, marker_ys, marker_colors, marker_labels = [], [], [], []
    for i, d in enumerate(decisions):
        if d != prev_decision:
            marker_xs.append(xs[i])
            marker_ys.append(ys[i])
            marker_colors.append(decision_colors.get(d, "#888"))
            marker_labels.append(d)
            prev_decision = d
    
    ax.scatter(marker_xs, marker_ys, c=marker_colors, s=120, zorder=5,
               edgecolors="white", linewidths=1.5)
    
    # Label the decision transitions
    for i, (mx, my, label) in enumerate(zip(marker_xs, marker_ys, marker_labels)):
        offset = 12 if i % 2 == 0 else -18
        ax.annotate(
            label.upper().replace("_", " "),
            (mx, my),
            textcoords="offset points",
            xytext=(10, offset),
            fontsize=7.5,
            fontweight="bold",
            color="white",
            alpha=0.9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=decision_colors.get(label, "#888"),
                      alpha=0.7, edgecolor="none"),
        )
    
    # --- Start / End markers ---
    ax.plot(xs[0], ys[0], "o", color="#22d3ee", markersize=14, zorder=6)
    ax.annotate("START", (xs[0], ys[0]), textcoords="offset points",
                xytext=(-30, 15), fontsize=9, fontweight="bold", color="#22d3ee")
    
    ax.plot(xs[-1], ys[-1], "s", color="#f43f5e", markersize=14, zorder=6)
    ax.annotate("END", (xs[-1], ys[-1]), textcoords="offset points",
                xytext=(10, -20), fontsize=9, fontweight="bold", color="#f43f5e")
    
    # --- Speed heatmap aura ---
    norm_speeds = (speeds - speeds.min()) / (speeds.max() - speeds.min() + 1e-6)
    scatter = ax.scatter(xs, ys, c=norm_speeds, cmap="coolwarm", s=2, alpha=0.3, zorder=2)
    
    # --- Legend ---
    legend_patches = [
        mpatches.Patch(color=c, label=d.replace("_", " ").title())
        for d, c in decision_colors.items()
    ]
    legend = ax.legend(handles=legend_patches, loc="upper left", fontsize=8,
                       facecolor="#1e293b", edgecolor="#334155", labelcolor="white",
                       title="Decisions", title_fontsize=9)
    legend.get_title().set_color("white")
    
    # --- Styling ---
    ax.set_title("Alpamayo R1 — Simulated Urban Trajectory & Decision Map",
                 fontsize=16, fontweight="bold", color="white", pad=15)
    ax.set_xlabel("X Position (m)", fontsize=11, color="#94a3b8")
    ax.set_ylabel("Y Position (m)", fontsize=11, color="#94a3b8")
    ax.tick_params(colors="#64748b")
    for spine in ax.spines.values():
        spine.set_color("#334155")
    ax.grid(True, alpha=0.1, color="#475569")
    ax.set_aspect("equal")
    
    # Subtitle
    ax.text(0.5, -0.08,
            "Kinematic Bicycle Model  •  Pure Pursuit Steering  •  PID Speed Control",
            transform=ax.transAxes, ha="center", fontsize=9, color="#64748b", style="italic")
    
    plt.tight_layout()
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "trajectory_decisions.png")
    fig.savefig(out_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved visualization to {out_path}")
    return out_path

if __name__ == "__main__":
    xs, ys, speeds, decisions, confidences = generate_trajectory()
    plot_trajectory(xs, ys, speeds, decisions, confidences)
