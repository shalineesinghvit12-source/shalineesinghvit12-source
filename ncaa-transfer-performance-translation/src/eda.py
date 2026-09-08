"""Exploratory analysis for team, player, and transfer demo data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def save(fig_name):
    plt.tight_layout()
    plt.savefig(OUT / fig_name, dpi=180)
    plt.close()


if __name__ == "__main__":
    teams = pd.read_csv(OUT / "team_seasons_clean.csv")
    players = pd.read_csv(OUT / "player_seasons_clean.csv")
    transfers = pd.read_csv(OUT / "transfers_clean.csv")

    # 1. Offensive Rating distribution
    plt.figure(figsize=(8, 5))
    plt.hist(teams["offensive_rating"], bins=15)
    plt.xlabel("Offensive Rating")
    plt.ylabel("Team-Seasons")
    plt.title("Distribution of Offensive Rating")
    save("eda_offensive_rating_distribution.png")

    # 2. Offensive vs Defensive Rating
    plt.figure(figsize=(8, 6))
    plt.scatter(teams["offensive_rating"], teams["defensive_rating"], alpha=0.65)
    plt.xlabel("Offensive Rating")
    plt.ylabel("Defensive Rating (lower is better)")
    plt.title("Team Offensive vs Defensive Efficiency")
    save("eda_offense_vs_defense.png")

    # 3. Average Net Rating by season
    seasonal = teams.groupby("season", as_index=False)["net_rating"].mean()
    plt.figure(figsize=(8, 5))
    plt.plot(seasonal["season"], seasonal["net_rating"], marker="o")
    plt.xlabel("Season")
    plt.ylabel("Average Net Rating")
    plt.title("Team Efficiency Across Seasons")
    save("eda_net_rating_by_season.png")

    # 4. Team metric correlation matrix
    corr_cols = [
        "offensive_rating", "defensive_rating", "net_rating", "pace", "efg_pct",
        "turnover_pct", "off_rebound_pct", "free_throw_rate", "strength_of_schedule_z",
    ]
    corr = teams[corr_cols].corr()
    plt.figure(figsize=(10, 8))
    plt.imshow(corr, aspect="auto")
    plt.xticks(range(len(corr_cols)), corr_cols, rotation=90)
    plt.yticks(range(len(corr_cols)), corr_cols)
    plt.colorbar()
    plt.title("Team Metric Correlation Matrix")
    save("eda_team_metric_correlation.png")

    # 5. PPG boxplot for player outlier review
    plt.figure(figsize=(7, 5))
    plt.boxplot(players["points_per_game"].dropna())
    plt.ylabel("Points Per Game")
    plt.title("Player PPG Distribution / Outlier Check")
    save("eda_player_ppg_boxplot.png")

    # 6. Pre vs post transfer PPG
    plt.figure(figsize=(8, 6))
    plt.scatter(transfers["pre_ppg"], transfers["post_ppg"], alpha=0.65)
    lo = min(transfers["pre_ppg"].min(), transfers["post_ppg"].min())
    hi = max(transfers["pre_ppg"].max(), transfers["post_ppg"].max())
    plt.plot([lo, hi], [lo, hi], linestyle="--")
    plt.xlabel("Pre-Transfer PPG")
    plt.ylabel("Post-Transfer PPG")
    plt.title("Pre vs Post Transfer Scoring")
    save("eda_pre_vs_post_ppg.png")

    print("EDA charts saved to outputs/.")
