# NCAA Transfer Performance Translation Model

A Python proof of concept for a college basketball analytics question: **how might a player's production translate when moving from one competitive team environment to another?**

The project combines team profiling, offensive/defensive efficiency, player-transfer history, comparable environments, and predictive modeling. It is designed around a recruiting/transfer-portal workflow where raw box-score production should be interpreted in the context of the player's source and destination environments.

> **Data note:** The repository ships with deterministic synthetic NCAA-like demo data generation so it can run end to end without redistributing proprietary, licensed, or scraped player data. The modeling pipeline is data-source agnostic and can be replaced with licensed/public historical data that follows the documented schema.

## Basketball question

A player can post strong numbers in one environment and face a different role, competition level, pace, spacing, defensive quality, and usage at the next school. This prototype asks:

1. What does each team's five-year statistical profile look like?
2. Can team environments be segmented into **Low / Medium / High** profiles using offensive, defensive, and style metrics?
3. How did historical players perform after moving between those profiles?
4. Can pre-transfer player production plus source/destination context predict post-transfer performance?

## Team profile features

- Offensive Rating: points scored per 100 possessions
- Defensive Rating: points allowed per 100 possessions
- Net Rating: Offensive Rating minus Defensive Rating
- Pace
- Effective field-goal percentage
- Turnover percentage
- Offensive rebound percentage
- Free-throw rate
- Strength-of-schedule proxy

K-means groups team-seasons into three statistical profiles. The clusters are ordered by average Net Rating and labeled Low, Medium, and High. This avoids assigning arbitrary rating cutoffs.

## Transfer model features

The model uses pre-transfer player production plus source and destination context:

- Minutes/game, PPG, Usage%, TS%, Assist%, Turnover%, Rebound%, player Offensive Rating
- Source team ORtg, DRtg, Net Rating, schedule strength, profile tier
- Destination team ORtg, DRtg, Net Rating, schedule strength, profile tier
- Position and transition type, e.g. `Low → High`

Targets in the prototype:

- Post-transfer player Offensive Rating
- Post-transfer True Shooting %
- Post-transfer PPG
- Post-transfer Usage %

Two model families are compared for each target: **Ridge Regression** and **Random Forest Regression**. The model with the lower held-out mean absolute error is selected.

## Why this design

The goal is not to claim that one metric can determine whether a transfer will succeed. The goal is to create a transparent decision-support framework that adjusts a player's prior production for the environment he is leaving and the environment he is entering.

A production version would add real transfer histories, opponent-adjusted metrics, role/lineup context, recruiting history, injuries/availability, coaching-system variables, and uncertainty intervals.

## Project structure

```text
.
├── app/
│   └── streamlit_app.py
├── src/
│   ├── generate_demo_data.py
│   ├── build_model.py
│   └── predict.py
├── run_pipeline.py
├── requirements.txt
└── .gitignore
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py
streamlit run app/streamlit_app.py
```

## Replace demo data with real data

The cleanest production path is to build three tables with the same roles as the included demo data:

1. `team_seasons`: one row per team-season with ORtg/DRtg and style metrics.
2. `player_seasons`: one row per player-team-season with advanced player metrics.
3. `transfers`: one row per school-to-school move linking the player's pre- and post-transfer seasons.

Potential public/research sources include Bart Torvik-derived datasets and college-basketball data packages. Always verify source terms before redistributing data.

## Decision-support interpretation

A useful staff-facing output should show:

- source profile and destination profile
- projected post-transfer efficiency/usage
- direction and magnitude of expected change
- historical transition averages
- comparable team/player examples when licensed data is available
- uncertainty and caveats

The output should support scouting discussion, not replace film study, coaching judgment, medical information, or direct player evaluation.
