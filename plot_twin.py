import matplotlib.pyplot as plt
import numpy as np

print("[Visualizer] Booting standalone diagnostics generator...")

# 1. Replicate the live degradation event seen in your stream logs
# (Dropping from ~92% down to 88.48% across timestamps)
timestamps = np.arange(100, 400)
health_history = []
ewma_history = []

# Statistical Process Control Limit matched to your system core
spc_limit = -0.035 

# Model state simulation logic
for t in timestamps:
    # Simulating the micro-stress vectors dropping health gradually
    if t < 200:
        h = 95.0 - (t - 100) * 0.03 + np.random.normal(0, 0.2)
        e = -0.01 + np.random.normal(0, 0.002)
    else:
        # Rapid transient deterioration phase pushing RUL fallback limits
        h = 92.0 - (t - 200) * 0.045 + np.random.normal(0, 0.4)
        e = -0.01 - (t - 200) * 0.00018 + np.random.normal(0, 0.003)
        
    health_history.append(max(0, h))
    ewma_history.append(e)

# 2. Generate high-fidelity diagnostic plot layout
print("[Visualizer] Compiling twin telemetry curves...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Composite Health & RUL Trajectory
ax1.plot(timestamps, health_history, color='#FF4B4B', linewidth=2, label='Dynamic Health Index')
ax1.axhline(25, color='orange', linestyle='--', linewidth=1.5, label='Critical Threshold (25%)')
# Pinpoint the exact state captured at your log timestamp 343
ax1.scatter(343, 88.48, color='black', s=100, zorder=5, label='Current Snapshot (88.48%)')
ax1.annotate('4.5 Hours Remaining\n(Linear Fallback Active)', xy=(343, 88.48), xytext=(220, 60),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))

ax1.set_title('🏭 Digital Twin Diagnostic Telemetry Report', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Asset Health (%)', fontsize=12)
ax1.set_ylim(0, 105)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='lower left')

# Bottom Plot: Mathematical Filter Layer (EWMA)
ax2.plot(timestamps, ewma_history, color='#1C83E1', linewidth=2, label='Smoothed EWMA Score')
ax2.axhline(spc_limit, color='red', linestyle=':', linewidth=2, label='3σ Lower Control Limit')
# Mirror log timestamp 343 metrics
ax2.scatter(343, -0.0247, color='black', s=100, zorder=5, label='EWMA: -0.0247')

ax2.set_xlabel('Data Stream Timestamps', fontsize=12)
ax2.set_ylabel('Anomaly Filter Score', fontsize=12)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower left')

plt.tight_layout()
output_path = 'twin_diagnostic_report.png'
plt.savefig(output_path, dpi=300)
print(f"[Visualizer] Success! Diagnostic image saved to: {output_path}")
