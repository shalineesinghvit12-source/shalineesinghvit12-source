"""Team profiling, comparable-player search, and transfer performance models.

Model families intentionally match the analytics coursework used in this project:
K-means, Linear Regression, Decision Tree, Random Forest, and KNN-style
nearest-neighbor similarity.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.neighbors import NearestNeighbors
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TEAM_FEATURES = [
    "offensive_rating", "defensive_rating", "pace", "efg_pct",
    "turnover_pct", "off_rebound_pct", "free_throw_rate",
    "strength_of_schedule_z"
]

NUM_FEATURES = [
    "pre_minutes", "pre_ppg", "pre_usage", "pre_ts", "pre_ast",
    "pre_tov", "pre_reb", "pre_player_ortg",
    "source_team_ortg", "source_team_drtg", "source_team_net", "source_sos_z",
    "dest_team_ortg", "dest_team_drtg", "dest_team_net", "dest_sos_z"
]
CAT_FEATURES = ["position", "source_tier", "dest_tier", "transition"]
TARGETS = ["post_player_ortg", "post_ts", "post_ppg", "post_usage"]


def clean_validate(teams: pd.DataFrame, transfers: pd.DataFrame):
    """Basic quality checks before analytics/modeling."""
    teams = teams.drop_duplicates(subset=["season", "team"]).copy()
    transfers = transfers.drop_duplicates().copy()

    required_team = ["season", "team", "offensive_rating", "defensive_rating"]
    required_transfer = ["player_id", "from_season", "to_season", "from_team", "to_team"]
    missing_team = [c for c in required_team if c not in teams.columns]
    missing_transfer = [c for c in required_transfer if c not in transfers.columns]
    if missing_team or missing_transfer:
        raise ValueError(f"Missing required columns. team={missing_team}, transfer={missing_transfer}")

    teams["team"] = teams["team"].astype(str).str.strip()
    transfers["from_team"] = transfers["from_team"].astype(str).str.strip()
    transfers["to_team"] = transfers["to_team"].astype(str).str.strip()

    if "net_rating" not in teams.columns:
        teams["net_rating"] = teams["offensive_rating"] - teams["defensive_rating"]

    teams = teams.dropna(subset=TEAM_FEATURES + ["net_rating"])
    transfers = transfers.dropna(subset=NUM_FEATURES + TARGETS)
    return teams, transfers


def profile_teams(teams: pd.DataFrame):
    """Standardize team metrics, run K-means, label clusters Low/Medium/High."""
    scaler = StandardScaler()
    Z = scaler.fit_transform(teams[TEAM_FEATURES])

    km = KMeans(n_clusters=3, n_init=30, random_state=42).fit(Z)
    prof = teams.copy()
    prof["cluster"] = km.labels_

    cluster_strength = prof.groupby("cluster")["net_rating"].mean().sort_values()
    tier_map = {
        cluster_strength.index[0]: "Low",
        cluster_strength.index[1]: "Medium",
        cluster_strength.index[2]: "High",
    }
    prof["tier"] = prof["cluster"].map(tier_map)
    prof["net_rating_percentile"] = prof["net_rating"].rank(pct=True).mul(100).round(1)

    nn = NearestNeighbors(metric="euclidean", n_neighbors=min(10, len(prof))).fit(Z)
    return prof, scaler, km, nn, Z


def attach_tiers(transfers: pd.DataFrame, prof: pd.DataFrame):
    src = prof[["season", "team", "tier"]].rename(
        columns={"season": "from_season", "team": "from_team", "tier": "source_tier"}
    )
    dst = prof[["season", "team", "tier"]].rename(
        columns={"season": "to_season", "team": "to_team", "tier": "dest_tier"}
    )
    x = transfers.merge(src, on=["from_season", "from_team"], how="left")
    x = x.merge(dst, on=["to_season", "to_team"], how="left")
    x["transition"] = x["source_tier"] + " → " + x["dest_tier"]
    return x.dropna(subset=CAT_FEATURES)


def make_pipeline(kind: str):
    prep = ColumnTransformer([
        ("num", StandardScaler(), NUM_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_FEATURES),
    ])

    if kind == "linear":
        model = LinearRegression()
    elif kind == "tree":
        model = DecisionTreeRegressor(max_depth=5, min_samples_leaf=10, random_state=42)
    elif kind == "rf":
        model = RandomForestRegressor(
            n_estimators=300, max_depth=8, min_samples_leaf=5,
            random_state=42, n_jobs=-1
        )
    else:
        raise ValueError(f"Unknown model kind: {kind}")

    return Pipeline([("prep", prep), ("model", model)])


def time_split(df: pd.DataFrame):
    """Train on earlier transfers and test on the latest destination season."""
    latest = df["to_season"].max()
    train_idx = np.flatnonzero((df["to_season"] < latest).to_numpy())
    test_idx = np.flatnonzero((df["to_season"] == latest).to_numpy())

    if len(train_idx) < 30 or len(test_idx) < 10:
        # Deterministic fallback for very small demonstration datasets.
        rng = np.random.default_rng(42)
        idx = np.arange(len(df))
        rng.shuffle(idx)
        cut = int(len(idx) * 0.75)
        return idx[:cut], idx[cut:], "random_75_25"
    return train_idx, test_idx, f"time_based_test_{int(latest)}"


def train_models(df: pd.DataFrame):
    """Compare Linear Regression, Decision Tree, and Random Forest by test MAE."""
    X = df[NUM_FEATURES + CAT_FEATURES]
    train_idx, test_idx, validation = time_split(df)

    results = {}
    selected_models = {}

    for target in TARGETS:
        y = df[target]
        candidates = {}

        for kind in ["linear", "tree", "rf"]:
            pipe = make_pipeline(kind)
            pipe.fit(X.iloc[train_idx], y.iloc[train_idx])
            pred = pipe.predict(X.iloc[test_idx])
            candidates[kind] = {
                "mae": float(mean_absolute_error(y.iloc[test_idx], pred)),
                "r2": float(r2_score(y.iloc[test_idx], pred)),
                "model": pipe,
            }

        best = min(candidates, key=lambda k: candidates[k]["mae"])
        selected_models[target] = candidates[best]["model"]
        results[target] = {
            "selected_model": best,
            "mae": round(candidates[best]["mae"], 3),
            "r2": round(candidates[best]["r2"], 3),
            "linear_mae": round(candidates["linear"]["mae"], 3),
            "tree_mae": round(candidates["tree"]["mae"], 3),
            "rf_mae": round(candidates["rf"]["mae"], 3),
            "validation": validation,
        }

    return selected_models, results


def build_player_similarity(df: pd.DataFrame):
    """KNN-style comparable-transfer engine using standardized numeric features."""
    similarity_features = [
        "pre_ppg", "pre_usage", "pre_ts", "pre_player_ortg",
        "source_team_net", "source_sos_z", "dest_team_net", "dest_sos_z"
    ]
    scaler = StandardScaler()
    matrix = scaler.fit_transform(df[similarity_features])
    nn = NearestNeighbors(n_neighbors=min(10, len(df)), metric="euclidean").fit(matrix)
    return scaler, nn, matrix, similarity_features


if __name__ == "__main__":
    teams = pd.read_csv(DATA / "team_seasons_demo.csv")
    transfers = pd.read_csv(DATA / "transfers_demo.csv")

    teams, transfers = clean_validate(teams, transfers)
    prof, scaler, km, team_nn, team_matrix = profile_teams(teams)
    trans = attach_tiers(transfers, prof)

    models, metrics = train_models(trans)
    player_scaler, player_nn, player_matrix, player_similarity_features = build_player_similarity(trans)

    prof.to_csv(OUT / "team_profiles.csv", index=False)
    trans.to_csv(OUT / "transfer_modeling_table.csv", index=False)

    with open(OUT / "model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    joblib.dump(
        {
            "team_scaler": scaler,
            "team_kmeans": km,
            "team_nearest_neighbors": team_nn,
            "team_matrix": team_matrix,
            "player_similarity_scaler": player_scaler,
            "player_nearest_neighbors": player_nn,
            "player_matrix": player_matrix,
            "player_similarity_features": player_similarity_features,
            "models": models,
        },
        OUT / "model_bundle.joblib",
    )

    summary = trans.groupby("transition").agg(
        n=("player_id", "size"),
        pre_ortg=("pre_player_ortg", "mean"),
        post_ortg=("post_player_ortg", "mean"),
        pre_ts=("pre_ts", "mean"),
        post_ts=("post_ts", "mean"),
        pre_ppg=("pre_ppg", "mean"),
        post_ppg=("post_ppg", "mean"),
    ).reset_index()
    summary["ortg_change"] = summary.post_ortg - summary.pre_ortg
    summary["ts_change"] = summary.post_ts - summary.pre_ts
    summary["ppg_change"] = summary.post_ppg - summary.pre_ppg
    summary.round(2).to_csv(OUT / "transition_summary.csv", index=False)

    print(json.dumps(metrics, indent=2))
    print("\nTransition summary:\n")
    print(summary.sort_values("n", ascending=False).round(2).to_string(index=False))
