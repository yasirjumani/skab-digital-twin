def print_pro_diagram():
    diagram = """
+------------------+      +---------------------+      +---------------------+      +---------------------+      +-----------------+
|    Ingestion     |----->| Feature Engineering |----->|   Model Inference   |----->|   Ensemble Fusion   |----->|      Alert      |
+------------------+      +---------------------+      +---------------------+      +---------------------+      +-----------------+
    """
    with open('pipeline_diagram_pro.txt', 'w') as f:
        f.write(diagram)
    print("Professional schematic saved to pipeline_diagram_pro.txt")

print_pro_diagram()
