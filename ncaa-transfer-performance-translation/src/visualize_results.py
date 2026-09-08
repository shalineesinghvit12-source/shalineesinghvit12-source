"""Generate portfolio-ready analytics charts for the README and outputs folder."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

NUM_FEATURES = [
    "pre_minutes", "pre_ppg", "pre_usage", "pre_ts", "pre_ast",
    "pre_tov", "pre_reb", "pre_player_ortg",
    "source_team_ortg", "source_team_drtg", "source_team_net", "source_sos_z",
    "dest_team_ortg", "dest_team_drtg", "dest_team_net", "dest_sos_z",
]


def team_profile_chart(prof):
    plt.figure(figsize=(9, 6))
    for tier in ["Low", "Medium", "High"]:
        d = prof[prof["tier"] == tier]
        plt.scatter(d["offensive_rating"], d["defensive_rating"], label=tier, alpha=0.65)
    plt.xlabel("Offensive Rating")
    plt.ylabel("Defensive Rating (lower is better)")
    plt.title("Team Environment Profiles: Offensive vs Defensive Efficiency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "team_profiles.png", dpi=180)
    plt.close()


def transition_chart(trans):
    summary = trans.groupby("transition").agg(
        n=("player_id", "size"),
        pre_ppg=("pre_ppg", "mean"),
        post_ppg=("post_ppg", "mean"),
        pre_ts=("pre_ts", "mean"),
        post_ts=("post_ts", "mean"),
        pre_ortg=("pre_player_ortg", "mean"),
        post_ortg=("post_player_ortg", "mean"),
    ).reset_index()
    summary["ppg_change"] = summary["post_ppg"] - summary["pre_ppg"]
    summary["ts_change"] = summary["post_ts"] - summary["pre_ts"]
    summary["ortg_change"] = summary["post_ortg"] - summary["pre_ortg"]

    preferred = ["Low → High", "Medium → High", "High → High"]
    selected = summary[summary["transition"].isin(preferred)].copy()
    if selected.empty:
        selected = summary.sort_values("n", ascending=False).head(5)

    x = np.arange(len(selected))
    width = 0.25
    plt.figure(figsize=(9, 6))
    plt.bar(x - width, selected["ppg_change"], width, label="PPG change")
    plt.bar(x, selected["ts_change"], width, label="TS% change")
    plt.bar(x + width, selected["ortg_change"], width, label="ORtg change")
    plt.axhline(0, linewidth=1)
    plt.xticks(x, selected["transition"], rotation=15)
    plt.ylabel("Average post-transfer change")
    plt.title("Historical Transfer Translation by Team Profile")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "transition_analysis.png", dpi=180)
    plt.close()


def model_comparison_chart(metrics):
    primary = metrics["post_player_ortg"]
    labels = ["Linear Regression", "Decision Tree", "Random Forest"]
    values = [primary["linear_mae"], primary["tree_mae"], primary["rf_mae"]]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.ylabel("MAE (lower is better)")
    plt.title("Post-Transfer Offensive Rating: Model Comparison")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(OUT / "model_comparison.png", dpi=180)
    plt.close()


def feature_importance_chart(trans):
    # Diagnostic view: fit a Random Forest on numeric features only so the chart
    # remains easy to explain even when another model wins the MAE comparison.
    X = trans[NUM_FEATURES]
    y = trans["post_player_ortg"]
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.25, random_state=42)
    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    importance = (
        pd.Series(rf.feature_importances_, index=NUM_FEATURES)
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )
    plt.figure(figsize=(9, 6))
    plt.barh(importance.index, importance.values)
    plt.xlabel("Random Forest feature importance")
    plt.title("Top Features for Post-Transfer Offensive Rating")
    plt.tight_layout()
    plt.savefig(OUT / "feature_importance.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    prof = pd.read_csv(OUT / "team_profiles.csv")
    trans = pd.read_csv(OUT / "transfer_modeling_table.csv")
    with open(OUT / "model_metrics.json") as f:
        metrics = json.load(f)

    team_profile_chart(prof)
    transition_chart(trans)
    model_comparison_chart(metrics)
    feature_importance_chart(trans)

    print("Saved portfolio charts to outputs/.")
