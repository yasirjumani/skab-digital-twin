import subprocess
import sys

def generate():
    # Use mermaid-cli via npx if available, otherwise suggest manual export
    try:
        subprocess.run(["npx", "-p", "@mermaid-js/mermaid-cli", "mmdc", "-i", "architecture.mmd", "-o", "SKAB_Pipeline_Architecture.png"], check=True)
        print("Successfully generated SKAB_Pipeline_Architecture.png")
    except Exception as e:
        print("Auto-generation failed. Please open architecture.mmd in VS Code and use 'Save as Image' from the Mermaid Preview.")

if __name__ == "__main__":
    generate()
