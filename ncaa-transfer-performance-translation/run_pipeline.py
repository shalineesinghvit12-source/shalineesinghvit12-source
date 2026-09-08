import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

scripts = [
    ROOT / "src" / "generate_demo_data.py",
    ROOT / "src" / "build_model.py",
    ROOT / "src" / "visualize_results.py",
]

for script in scripts:
    subprocess.run([sys.executable, str(script)], check=True)

print("\nPipeline complete.")
print("Charts and model outputs are in outputs/.")
print("Launch the dashboard with: streamlit run app/streamlit_app.py")
