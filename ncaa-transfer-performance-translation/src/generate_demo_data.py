"""Generate a deterministic, NCAA-like five-season demo dataset.

This is intentionally synthetic so the public portfolio does not redistribute
proprietary or licensed player data. The pipeline is data-source agnostic:
replace the generated CSVs with licensed/public NCAA data using the same schema.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

SEASONS = [2021, 2022, 2023, 2024, 2025]
N_TEAMS = 96
N_PLAYERS_PER_TEAM = 11

FIRST = ["Alex","Jordan","Chris","Taylor","Cameron","Drew","Sam","Devin","Marcus","Eli","Noah","Malik","Jalen","Avery","Miles","Tyler","Ryan","Cole"]
LAST = ["Brown","Davis","Smith","Johnson","Williams","Miller","Wilson","Moore","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin","Clark","Lewis","Walker"]
POSITIONS = ["PG","SG","SF","PF","C"]


def clip(x, lo, hi):
    return np.clip(x, lo, hi)


def make_team_rows():
    rows=[]
    base_strength = rng.normal(0, 1, N_TEAMS)
    styles = rng.normal(0, 0.75, (N_TEAMS, 4))
    team_names = [f"Program {i+1:02d}" for i in range(N_TEAMS)]
    for season in SEASONS:
        season_shift = rng.normal(0, 0.15, N_TEAMS)
        strength = 0.82*base_strength + season_shift + rng.normal(0,0.22,N_TEAMS)
        for i, team in enumerate(team_names):
            s = strength[i]
            pace = clip(68 + 1.8*styles[i,0] + rng.normal(0,1.7), 61, 77)
            ortg = 108 + 6.8*s + 1.3*styles[i,1] + rng.normal(0,1.7)
            drtg = 108 - 6.3*s + 1.2*styles[i,2] + rng.normal(0,1.8)
            efg = clip(50.5 + 2.8*s + 0.9*styles[i,1] + rng.normal(0,1.0), 43, 61)
            tov = clip(19.2 - 1.4*s + 0.5*styles[i,3] + rng.normal(0,0.8), 13, 25)
            orb = clip(28.5 + 1.5*s + rng.normal(0,1.6), 20, 39)
            ftr = clip(30 + 1.3*styles[i,3] + rng.normal(0,2.5), 18, 45)
            sos = clip(0.05 + 0.72*s + rng.normal(0,0.42), -2.2, 2.4)
            rows.append({
                "season": season, "team": team,
                "offensive_rating": round(ortg,2), "defensive_rating": round(drtg,2),
                "net_rating": round(ortg-drtg,2), "pace": round(pace,2),
                "efg_pct": round(efg,2), "turnover_pct": round(tov,2),
                "off_rebound_pct": round(orb,2), "free_throw_rate": round(ftr,2),
                "strength_of_schedule_z": round(sos,3)
            })
    return pd.DataFrame(rows)


def make_player_rows(team_df):
    rows=[]
    pid=1
    team_strength = team_df.set_index(["season","team"])["net_rating"].to_dict()
    teams = sorted(team_df.team.unique())
    player_ids_by_team = {t: [] for t in teams}
    for t in teams:
        for _ in range(N_PLAYERS_PER_TEAM):
            player_ids_by_team[t].append(pid); pid+=1

    active = {t:list(ids) for t,ids in player_ids_by_team.items()}
    player_meta = {}
    for t,ids in active.items():
        for p in ids:
            player_meta[p] = {
                "name": f"{rng.choice(FIRST)} {rng.choice(LAST)} {p}",
                "position": rng.choice(POSITIONS, p=[.22,.23,.20,.19,.16]),
                "ability": rng.normal(0,1), "experience": rng.integers(1,4)
            }

    next_pid=pid
    for season in SEASONS:
        if season != SEASONS[0]:
            all_pairs=[(t,p) for t,ids in active.items() for p in ids]
            transfer_set=set(p for _,p in rng.choice(np.array(all_pairs,dtype=object), size=int(len(all_pairs)*0.20), replace=False))
            new_active={t:[] for t in teams}
            for t,ids in active.items():
                for p in ids:
                    if p not in transfer_set:
                        new_active[t].append(p)
                    else:
                        src_net = team_strength[(season-1,t)]
                        candidates=[tt for tt in teams if tt!=t]
                        weights=np.array([np.exp(-abs(team_strength[(season,tt)]-(src_net+rng.normal(2.5,7)))/7) for tt in candidates])
                        dest=rng.choice(candidates,p=weights/weights.sum())
                        new_active[dest].append(p)
            for t in teams:
                while len(new_active[t]) < N_PLAYERS_PER_TEAM:
                    p=next_pid; next_pid+=1
                    new_active[t].append(p)
                    player_meta[p] = {"name":f"{rng.choice(FIRST)} {rng.choice(LAST)} {p}","position":rng.choice(POSITIONS,p=[.22,.23,.20,.19,.16]),"ability":rng.normal(-0.1,1),"experience":1}
                if len(new_active[t])>13:
                    new_active[t]=new_active[t][:13]
            active=new_active

        for team, ids in active.items():
            tnet=team_strength[(season,team)]
            context = tnet/12.0
            for p in ids:
                m=player_meta[p]
                abil=m["ability"] + 0.12*(m["experience"]-1)
                pos=m["position"]
                minutes=clip(19 + 6.0*abil + 1.3*context + rng.normal(0,4), 4, 36)
                usage=clip(18 + 4.2*abil - 0.8*context + rng.normal(0,2.0), 8, 32)
                ts=clip(54 + 3.3*abil + 0.7*context + rng.normal(0,2.0), 42, 68)
                ast_base={"PG":24,"SG":15,"SF":11,"PF":8,"C":7}[pos]
                reb_base={"PG":6,"SG":7,"SF":10,"PF":15,"C":20}[pos]
                ast=clip(ast_base + 3.0*abil + rng.normal(0,3),2,38)
                tov=clip(17 - 1.8*abil + 0.5*usage/10 + rng.normal(0,1.5),8,28)
                reb=clip(reb_base + 2.1*abil + rng.normal(0,2.0),2,29)
                ortg=clip(102 + 5.7*abil + 1.4*context + 0.36*(ts-54) -0.28*(tov-17) + rng.normal(0,2.1),80,135)
                ppg=clip(minutes/30 * (9.0 + 0.55*usage + 0.10*(ts-54) + 1.2*abil) + rng.normal(0,1.0),1,29)
                rows.append({"player_id":p,"player":m["name"],"season":season,"team":team,"position":pos,
                             "minutes_per_game":round(minutes,2),"points_per_game":round(ppg,2),"usage_pct":round(usage,2),
                             "true_shooting_pct":round(ts,2),"assist_pct":round(ast,2),"turnover_pct":round(tov,2),
                             "rebound_pct":round(reb,2),"player_offensive_rating":round(ortg,2)})
                m["experience"] += 1
    return pd.DataFrame(rows)


def build_transfers(player_df, team_df):
    p = player_df.sort_values(["player_id","season"]).copy()
    prev=p.groupby("player_id").shift(1)
    mask=(prev["team"].notna()) & (p["team"] != prev["team"])
    cur=p[mask].copy().reset_index(drop=True)
    prv=prev[mask].reset_index(drop=True)
    tm=team_df.set_index(["season","team"])
    rows=[]
    for i,row in cur.iterrows():
        rprev=prv.iloc[i]
        src_season=int(rprev["season"]); dst_season=int(row["season"])
        src=tm.loc[(src_season,rprev["team"])]
        dst=tm.loc[(dst_season,row["team"])]
        rows.append({
            "player_id":int(row.player_id),"player":row.player,"position":row.position,
            "from_season":src_season,"to_season":dst_season,"from_team":rprev["team"],"to_team":row.team,
            "pre_minutes":rprev["minutes_per_game"],"pre_ppg":rprev["points_per_game"],"pre_usage":rprev["usage_pct"],
            "pre_ts":rprev["true_shooting_pct"],"pre_ast":rprev["assist_pct"],"pre_tov":rprev["turnover_pct"],
            "pre_reb":rprev["rebound_pct"],"pre_player_ortg":rprev["player_offensive_rating"],
            "source_team_ortg":src.offensive_rating,"source_team_drtg":src.defensive_rating,"source_team_net":src.net_rating,
            "source_sos_z":src.strength_of_schedule_z,
            "dest_team_ortg":dst.offensive_rating,"dest_team_drtg":dst.defensive_rating,"dest_team_net":dst.net_rating,
            "dest_sos_z":dst.strength_of_schedule_z,
            "post_minutes":row.minutes_per_game,"post_ppg":row.points_per_game,"post_usage":row.usage_pct,
            "post_ts":row.true_shooting_pct,"post_player_ortg":row.player_offensive_rating,
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    teams=make_team_rows(); players=make_player_rows(teams); transfers=build_transfers(players,teams)
    teams.to_csv(DATA/"team_seasons_demo.csv",index=False)
    players.to_csv(DATA/"player_seasons_demo.csv",index=False)
    transfers.to_csv(DATA/"transfers_demo.csv",index=False)
    print(f"team-seasons: {len(teams):,}; player-seasons: {len(players):,}; transfers: {len(transfers):,}")
