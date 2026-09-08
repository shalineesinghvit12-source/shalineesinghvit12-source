from pathlib import Path
import pandas as pd, joblib
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"outputs"
BUNDLE=joblib.load(OUT/"model_bundle.joblib")

def project_player(row: dict):
    x=pd.DataFrame([row])
    return {target: round(float(model.predict(x)[0]),2) for target,model in BUNDLE["models"].items()}
