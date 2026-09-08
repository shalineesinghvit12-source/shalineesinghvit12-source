from pathlib import Path
import sys
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from predict import project_player, find_comparable_transfers

OUT = ROOT / "outputs"

prof = pd.read_csv(OUT / "team_profiles.csv")
trans = pd.read_csv(OUT / "transfer_modeling_table.csv")
with open(OUT / "model_metrics.json") as f:
    metrics = json.load(f)

st.set_page_config(page_title="NCAA Transfer Translation", layout="wide")
st.title("NCAA Transfer Performance Translation")
st.caption(
    "Decision-support prototype using synthetic NCAA-like demo data. "
    "The same pipeline can be retrained on validated historical team, player, and transfer data."
)

st.subheader("1. Destination environment")
season = int(st.selectbox("Destination season", sorted(prof.season.unique(), reverse=True)))
team_names = sorted(prof.loc[prof.season == season, "team"].unique())
dest = st.selectbox("Destination team", team_names)
destrow = prof[(prof.season == season) & (prof.team == dest)].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Destination Tier", destrow.tier)
c2.metric("Offensive Rating", f"{destrow.offensive_rating:.1f}")
c3.metric("Defensive Rating", f"{destrow.defensive_rating:.1f}")
c4.metric("Net Rating", f"{destrow.net_rating:+.1f}")

st.subheader("2. Candidate player and source environment")
c1, c2, c3, c4 = st.columns(4)
position = c1.selectbox("Position", ["PG", "SG", "SF", "PF", "C"])
source_tier = c2.selectbox("Source tier", ["Low", "Medium", "High"])
pre_ppg = c3.number_input("Pre-transfer PPG", 1.0, 35.0, 15.0)
pre_min = c4.number_input("Minutes/game", 4.0, 40.0, 29.0)

c1, c2, c3, c4 = st.columns(4)
pre_usage = c1.number_input("Usage %", 5.0, 40.0, 23.0)
pre_ts = c2.number_input("True Shooting %", 35.0, 75.0, 56.0)
pre_ortg = c3.number_input("Player ORtg", 75.0, 140.0, 112.0)
pre_ast = c4.number_input("Assist %", 1.0, 45.0, 16.0)

c1, c2, c3, c4 = st.columns(4)
pre_tov = c1.number_input("Turnover %", 5.0, 35.0, 16.0)
pre_reb = c2.number_input("Rebound %", 1.0, 35.0, 9.0)
src_ortg = c3.number_input("Source Team ORtg", 85.0, 135.0, 106.0)
src_drtg = c4.number_input("Source Team DRtg", 85.0, 135.0, 112.0)

source_sos = st.slider(
    "Source strength-of-schedule z-score", -2.5, 2.5, -0.5, 0.1
)

if st.button("Project translation", type="primary"):
    row = {
        "pre_minutes": pre_min,
        "pre_ppg": pre_ppg,
        "pre_usage": pre_usage,
        "pre_ts": pre_ts,
        "pre_ast": pre_ast,
        "pre_tov": pre_tov,
        "pre_reb": pre_reb,
        "pre_player_ortg": pre_ortg,
        "source_team_ortg": src_ortg,
        "source_team_drtg": src_drtg,
        "source_team_net": src_ortg - src_drtg,
        "source_sos_z": source_sos,
        "dest_team_ortg": destrow.offensive_rating,
        "dest_team_drtg": destrow.defensive_rating,
        "dest_team_net": destrow.net_rating,
        "dest_sos_z": destrow.strength_of_schedule_z,
        "position": position,
        "source_tier": source_tier,
        "dest_tier": destrow.tier,
        "transition": f"{source_tier} → {destrow.tier}",
    }

    prediction = project_player(row)

    st.subheader("3. Projected post-transfer performance")
    cols = st.columns(4)
    cols[0].metric("Projected Player ORtg", prediction["post_player_ortg"])
    cols[1].metric("Projected TS%", prediction["post_ts"])
    cols[2].metric("Projected PPG", prediction["post_ppg"])
    cols[3].metric("Projected Usage%", prediction["post_usage"])

    primary = metrics["post_player_ortg"]
    st.caption(
        f"Primary ORtg model selected by held-out MAE: "
        f"{primary['selected_model'].replace('_', ' ').title()} "
        f"(MAE {primary['mae']:.2f}, R² {primary['r2']:.2f})."
    )

    st.subheader("4. Comparable historical transfers")
    comparable = find_comparable_transfers(row, trans, n_neighbors=5)
    st.dataframe(comparable, use_container_width=True)

    st.info(
        "Use the projection and comparables as decision-support signals. "
        "A production version should be retrained and validated on real historical transfers "
        "and supplemented by film, role/lineup fit, coaching system, availability, and scouting judgment."
    )

st.subheader("Historical transition summary")
st.dataframe(pd.read_csv(OUT / "transition_summary.csv"), use_container_width=True)

st.subheader("Model comparison")
model_rows = []
for target, values in metrics.items():
    model_rows.append({
        "Target": target,
        "Selected model": values["selected_model"],
        "MAE": values["mae"],
        "R²": values["r2"],
        "Linear MAE": values["linear_mae"],
        "Tree MAE": values["tree_mae"],
        "Random Forest MAE": values["rf_mae"],
    })
st.dataframe(pd.DataFrame(model_rows), use_container_width=True)
