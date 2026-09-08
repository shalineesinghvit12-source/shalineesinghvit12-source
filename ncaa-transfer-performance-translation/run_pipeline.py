import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Demo CSVs are committed in data/. The pipeline starts from those files just as
# a production version would start from validated historical source files.
scripts = [
    ROOT / "src" / "clean_data.py",
    ROOT / "src" / "eda.py",
    ROOT / "src" / "build_model.py",
    ROOT / "src" / "visualize_results.py",
]

for script in scripts:
    subprocess.run([sys.executable, str(script)], check=True)

print("\nPipeline complete.")
print("Cleaned data, charts, model metrics, and transition outputs are in outputs/.")
print("Launch the dashboard with: streamlit run app/streamlit_app.py")
