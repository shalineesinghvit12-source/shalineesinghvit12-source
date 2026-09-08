"""Team profiling, comparable-team search and transfer performance models."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.neighbors import NearestNeighbors
import joblib

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
TEAM_FEATURES=["offensive_rating","defensive_rating","pace","efg_pct","turnover_pct","off_rebound_pct","free_throw_rate","strength_of_schedule_z"]
NUM_FEATURES=["pre_minutes","pre_ppg","pre_usage","pre_ts","pre_ast","pre_tov","pre_reb","pre_player_ortg",
              "source_team_ortg","source_team_drtg","source_team_net","source_sos_z",
              "dest_team_ortg","dest_team_drtg","dest_team_net","dest_sos_z"]
CAT_FEATURES=["position","source_tier","dest_tier","transition"]
TARGETS=["post_player_ortg","post_ts","post_ppg","post_usage"]


def profile_teams(teams: pd.DataFrame):
    scaler=StandardScaler(); Z=scaler.fit_transform(teams[TEAM_FEATURES])
    km=KMeans(n_clusters=3,n_init=30,random_state=42).fit(Z)
    prof=teams.copy(); prof["cluster"]=km.labels_
    cluster_strength=prof.groupby("cluster")["net_rating"].mean().sort_values()
    tier_map={cluster_strength.index[0]:"Low",cluster_strength.index[1]:"Medium",cluster_strength.index[2]:"High"}
    prof["tier"]=prof["cluster"].map(tier_map)
    prof["net_rating_percentile"]=prof["net_rating"].rank(pct=True).mul(100).round(1)
    nn=NearestNeighbors(metric="euclidean").fit(Z)
    return prof, scaler, km, nn, Z


def attach_tiers(transfers, prof):
    src=prof[["season","team","tier"]].rename(columns={"season":"from_season","team":"from_team","tier":"source_tier"})
    dst=prof[["season","team","tier"]].rename(columns={"season":"to_season","team":"to_team","tier":"dest_tier"})
    x=transfers.merge(src,on=["from_season","from_team"],how="left").merge(dst,on=["to_season","to_team"],how="left")
    x["transition"]=x["source_tier"]+" → "+x["dest_tier"]
    return x


def make_pipeline(kind="ridge"):
    prep=ColumnTransformer([("num",StandardScaler(),NUM_FEATURES),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),CAT_FEATURES)])
    model=Ridge(alpha=4.0) if kind=="ridge" else RandomForestRegressor(n_estimators=300,min_samples_leaf=5,random_state=42,n_jobs=-1)
    return Pipeline([("prep",prep),("model",model)])


def train_models(df):
    X=df[NUM_FEATURES+CAT_FEATURES]; results={}; models={}
    train_idx,test_idx=train_test_split(np.arange(len(df)),test_size=.25,random_state=42)
    for target in TARGETS:
        y=df[target]
        candidates={}
        for kind in ["ridge","rf"]:
            pipe=make_pipeline(kind); pipe.fit(X.iloc[train_idx],y.iloc[train_idx]); pred=pipe.predict(X.iloc[test_idx])
            candidates[kind]=(mean_absolute_error(y.iloc[test_idx],pred),r2_score(y.iloc[test_idx],pred),pipe)
        best=min(candidates,key=lambda k:candidates[k][0])
        mae,r2,pipe=candidates[best]; models[target]=pipe
        results[target]={"selected_model":best,"mae":round(float(mae),3),"r2":round(float(r2),3),
                         "ridge_mae":round(float(candidates['ridge'][0]),3),"rf_mae":round(float(candidates['rf'][0]),3)}
    return models,results

if __name__=="__main__":
    teams=pd.read_csv(DATA/"team_seasons_demo.csv"); transfers=pd.read_csv(DATA/"transfers_demo.csv")
    prof, scaler, km, nn, Z=profile_teams(teams)
    trans=attach_tiers(transfers,prof)
    models,metrics=train_models(trans)
    prof.to_csv(OUT/"team_profiles.csv",index=False); trans.to_csv(OUT/"transfer_modeling_table.csv",index=False)
    with open(OUT/"model_metrics.json","w") as f: json.dump(metrics,f,indent=2)
    joblib.dump({"team_scaler":scaler,"team_kmeans":km,"nearest_neighbors":nn,"team_matrix":Z,"models":models},OUT/"model_bundle.joblib")
    summary=trans.groupby("transition").agg(n=("player_id","size"),pre_ortg=("pre_player_ortg","mean"),post_ortg=("post_player_ortg","mean"),pre_ts=("pre_ts","mean"),post_ts=("post_ts","mean"),pre_ppg=("pre_ppg","mean"),post_ppg=("post_ppg","mean")).reset_index()
    summary["ortg_change"]=summary.post_ortg-summary.pre_ortg; summary["ts_change"]=summary.post_ts-summary.pre_ts; summary["ppg_change"]=summary.post_ppg-summary.pre_ppg
    summary.round(2).to_csv(OUT/"transition_summary.csv",index=False)
    print(json.dumps(metrics,indent=2)); print("\nTransitions:\n",summary.sort_values("n",ascending=False).head(9).round(2).to_string(index=False))
