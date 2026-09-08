import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for script in [ROOT/"src"/"generate_demo_data.py",ROOT/"src"/"build_model.py"]:
    subprocess.run([sys.executable,str(script)],check=True)
print("\nDone. Launch dashboard with: streamlit run app/streamlit_app.py")
