from pathlib import Path
import sys, json
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/"src"))
from predict import project_player

OUT=ROOT/"outputs"
prof=pd.read_csv(OUT/"team_profiles.csv")
trans=pd.read_csv(OUT/"transfer_modeling_table.csv")
metrics=json.load(open(OUT/"model_metrics.json"))

st.set_page_config(page_title="NCAA Transfer Translation",layout="wide")
st.title("NCAA Transfer Performance Translation Prototype")
st.caption("Proof of concept using synthetic NCAA-like data. Designed to be replaced with licensed/public historical data.")

season=int(st.selectbox("Destination season",sorted(prof.season.unique(),reverse=True)))
teams=sorted(prof.loc[prof.season==season,"team"].unique())
dest=st.selectbox("Destination team profile",teams)
destrow=prof[(prof.season==season)&(prof.team==dest)].iloc[0]

c1,c2,c3=st.columns(3); c1.metric("Destination Tier",destrow.tier); c2.metric("Offensive Rating",destrow.offensive_rating); c3.metric("Defensive Rating",destrow.defensive_rating)

st.subheader("Player inputs")
c1,c2,c3,c4=st.columns(4)
position=c1.selectbox("Position",["PG","SG","SF","PF","C"]); source_tier=c2.selectbox("Source tier",["Low","Medium","High"]); pre_ppg=c3.number_input("Pre-transfer PPG",1.0,35.0,15.0); pre_min=c4.number_input("Minutes/game",4.0,40.0,29.0)
c1,c2,c3,c4=st.columns(4)
pre_usage=c1.number_input("Usage %",5.0,40.0,23.0); pre_ts=c2.number_input("True Shooting %",35.0,75.0,56.0); pre_ortg=c3.number_input("Player ORtg",75.0,140.0,112.0); pre_ast=c4.number_input("Assist %",1.0,45.0,16.0)
c1,c2,c3,c4=st.columns(4)
pre_tov=c1.number_input("Turnover %",5.0,35.0,16.0); pre_reb=c2.number_input("Rebound %",1.0,35.0,9.0); src_ortg=c3.number_input("Source Team ORtg",85.0,135.0,106.0); src_drtg=c4.number_input("Source Team DRtg",85.0,135.0,112.0)
source_sos=st.slider("Source strength-of-schedule z-score",-2.5,2.5,-0.5,.1)

if st.button("Project translation",type="primary"):
    row={"pre_minutes":pre_min,"pre_ppg":pre_ppg,"pre_usage":pre_usage,"pre_ts":pre_ts,"pre_ast":pre_ast,"pre_tov":pre_tov,"pre_reb":pre_reb,"pre_player_ortg":pre_ortg,
         "source_team_ortg":src_ortg,"source_team_drtg":src_drtg,"source_team_net":src_ortg-src_drtg,"source_sos_z":source_sos,
         "dest_team_ortg":destrow.offensive_rating,"dest_team_drtg":destrow.defensive_rating,"dest_team_net":destrow.net_rating,"dest_sos_z":destrow.strength_of_schedule_z,
         "position":position,"source_tier":source_tier,"dest_tier":destrow.tier,"transition":f"{source_tier} → {destrow.tier}"}
    pred=project_player(row)
    cols=st.columns(4)
    cols[0].metric("Projected Player ORtg",pred["post_player_ortg"])
    cols[1].metric("Projected TS%",pred["post_ts"])
    cols[2].metric("Projected PPG",pred["post_ppg"])
    cols[3].metric("Projected Usage%",pred["post_usage"])
    st.info("Use the projection as a decision-support signal, not a deterministic forecast. A production version should add real historical transfers, role context, injury/availability and coaching-system variables.")

st.subheader("Historical transition summary")
st.dataframe(pd.read_csv(OUT/"transition_summary.csv"),use_container_width=True)
