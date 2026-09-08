"""Clean and validate the committed demo inputs.

The public repository starts from pre-generated demo CSVs in data/. In a real
version, replace those files with validated historical team/player/transfer
exports that follow the documented schema.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

TEAM_FILE = DATA / "team_seasons_demo.csv"
TRANSFER_FILE = DATA / "transfers_demo.csv"
PLAYER_FILE = DATA / "player_seasons_demo.csv.gz"

TEAM_REQUIRED = [
    "season", "team", "offensive_rating", "defensive_rating", "pace",
    "efg_pct", "turnover_pct", "off_rebound_pct", "free_throw_rate",
    "strength_of_schedule_z",
]

TRANSFER_REQUIRED = [
    "player_id", "position", "from_season", "to_season", "from_team", "to_team",
    "pre_minutes", "pre_ppg", "pre_usage", "pre_ts", "pre_ast", "pre_tov",
    "pre_reb", "pre_player_ortg", "source_team_ortg", "source_team_drtg",
    "source_team_net", "source_sos_z", "dest_team_ortg", "dest_team_drtg",
    "dest_team_net", "dest_sos_z", "post_ppg", "post_usage", "post_ts",
    "post_player_ortg",
]


def require_columns(df: pd.DataFrame, columns, label: str):
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def clean_teams(df: pd.DataFrame) -> pd.DataFrame:
    require_columns(df, TEAM_REQUIRED, "team data")
    x = df.copy()
    x["team"] = x["team"].astype(str).str.strip()
    x = x.drop_duplicates(subset=["season", "team"])
    if "net_rating" not in x.columns:
        x["net_rating"] = x["offensive_rating"] - x["defensive_rating"]
    x = x.dropna(subset=TEAM_REQUIRED + ["net_rating"])
    return x.sort_values(["season", "team"]).reset_index(drop=True)


def clean_transfers(df: pd.DataFrame) -> pd.DataFrame:
    require_columns(df, TRANSFER_REQUIRED, "transfer data")
    x = df.copy()
    for c in ["from_team", "to_team", "position"]:
        x[c] = x[c].astype(str).str.strip()
    x["position"] = x["position"].str.upper()
    x = x.drop_duplicates()
    x = x.dropna(subset=TRANSFER_REQUIRED)
    return x.sort_values(["to_season", "player_id"]).reset_index(drop=True)


def clean_players(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    for c in ["player", "team", "position"]:
        if c in x.columns:
            x[c] = x[c].astype(str).str.strip()
    if "position" in x.columns:
        x["position"] = x["position"].str.upper()
    if {"player_id", "season", "team"}.issubset(x.columns):
        x = x.drop_duplicates(subset=["player_id", "season", "team"])
    return x.reset_index(drop=True)


if __name__ == "__main__":
    teams = clean_teams(pd.read_csv(TEAM_FILE))
    transfers = clean_transfers(pd.read_csv(TRANSFER_FILE))
    players = clean_players(pd.read_csv(PLAYER_FILE, compression="gzip"))

    teams.to_csv(OUT / "team_seasons_clean.csv", index=False)
    transfers.to_csv(OUT / "transfers_clean.csv", index=False)
    players.to_csv(OUT / "player_seasons_clean.csv", index=False)

    quality = pd.DataFrame({
        "table": ["team_seasons", "player_seasons", "transfers"],
        "rows_after_cleaning": [len(teams), len(players), len(transfers)],
        "missing_cells": [int(teams.isna().sum().sum()), int(players.isna().sum().sum()), int(transfers.isna().sum().sum())],
    })
    quality.to_csv(OUT / "data_quality_summary.csv", index=False)
    print(quality.to_string(index=False))
