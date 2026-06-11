import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw():
    fig, ax = plt.subplots(figsize=(16, 2.5))
    stages = ["Ingestion", "Feature Engineering", "Model Inference", "Ensemble Fusion", "Alerting"]
    x_pos = [0, 3.4, 6.8, 10.2, 13.6]
    
    for i, stage in enumerate(stages):
        ax.add_patch(patches.FancyBboxPatch((x_pos[i], 0.3), 3.0, 0.8, boxstyle="round,pad=0.2", fc="#F8F9FA", ec="#212529", lw=2))
        ax.text(x_pos[i] + 1.5, 0.7, stage, ha='center', va='center', fontweight='bold', fontsize=12)
        if i < len(stages) - 1:
            ax.annotate("", xy=(x_pos[i+1], 0.7), xytext=(x_pos[i] + 3.0, 0.7), arrowprops=dict(arrowstyle="->", color="#343A40", lw=2.5))
    
    ax.set_xlim(-0.5, 17)
    ax.set_ylim(0, 1.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('SKAB_Pipeline_Architecture.png', dpi=600, bbox_inches='tight')
    print("SUCCESS: SKAB_Pipeline_Architecture.png created.")

draw()
