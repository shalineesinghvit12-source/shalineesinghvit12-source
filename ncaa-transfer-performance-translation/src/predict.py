"""Prediction and comparable-player helpers for the transfer translation prototype."""
from pathlib import Path
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

BUNDLE = joblib.load(OUT / "model_bundle.joblib")


def project_player(row: dict):
    """Return post-transfer projections from the selected model for each target."""
    x = pd.DataFrame([row])
    return {
        target: round(float(model.predict(x)[0]), 2)
        for target, model in BUNDLE["models"].items()
    }


def find_comparable_transfers(row: dict, transfer_df: pd.DataFrame, n_neighbors: int = 5):
    """Return the most statistically similar historical transfer rows."""
    features = BUNDLE["player_similarity_features"]
    scaler = BUNDLE["player_similarity_scaler"]
    nn = BUNDLE["player_nearest_neighbors"]

    candidate = pd.DataFrame([{feature: row[feature] for feature in features}])
    candidate_scaled = scaler.transform(candidate)
    k = min(n_neighbors, len(transfer_df))
    distances, indices = nn.kneighbors(candidate_scaled, n_neighbors=k)

    cols = [
        "player_id", "position", "from_team", "to_team", "transition",
        "pre_ppg", "post_ppg", "pre_ts", "post_ts",
        "pre_player_ortg", "post_player_ortg",
    ]
    available = [c for c in cols if c in transfer_df.columns]
    result = transfer_df.iloc[indices[0]][available].copy()
    result.insert(0, "similarity_distance", distances[0].round(3))
    return result.reset_index(drop=True)
