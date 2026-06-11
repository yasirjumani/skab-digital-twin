import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_professional_pipeline():
    fig, ax = plt.subplots(figsize=(14, 3))
    stages = ["Ingestion", "Feature Engineering", "Model Inference", "Ensemble Fusion", "Alerting"]
    colors = ['#f8f9fa'] * 5
    
    for i, stage in enumerate(stages):
        # Draw professional box
        ax.add_patch(patches.FancyBboxPatch((i*2.4, 0.4), 2.0, 0.7, boxstyle="round,pad=0.1", 
                                            fc=colors[i], ec='#343a40', lw=2))
        ax.text(i*2.4 + 1.0, 0.75, stage, ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Draw clean arrow
        if i < len(stages) - 1:
            ax.annotate("", xy=(i*2.4 + 4.4, 0.75), xytext=(i*2.4 + 2.0, 0.75),
                        arrowprops=dict(arrowstyle="->", color='#495057', lw=2.5))
    
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 1.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('pipeline_diagram_pro.png', dpi=300, bbox_inches='tight')
    print("Professional diagram saved as pipeline_diagram_pro.png")

draw_professional_pipeline()
