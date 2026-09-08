# NCAA Transfer Performance Translation Model

A Python basketball analytics proof of concept for the question:

> **How might a player's performance translate when moving from one competitive team environment to another?**

The project is designed around a transfer-portal / recruiting workflow. It combines data cleaning, exploratory analysis, offensive/defensive team profiling, historical transfer analysis, comparable-player search, and predictive modeling.

> **Portfolio data note:** The repository includes deterministic synthetic NCAA-like demo data so the workflow can run end to end without redistributing licensed or proprietary data. The same pipeline is designed to accept real historical team, player-season, and transfer datasets when available.

## Business questions

1. What do team environments look like over multiple seasons?
2. Can teams be segmented into **Low / Medium / High** statistical profiles?
3. What historically happens when players move Low → High, Medium → High, High → High, etc.?
4. Which pre-transfer player and team-context features are most useful for explaining post-transfer performance?
5. Can historical data estimate post-transfer Offensive Rating, True Shooting %, PPG, and Usage %?
6. Which historical transfers are most similar to a current candidate?

## End-to-end analytics workflow

### 1. Data ingestion
Expected real-world tables:

- `team_seasons`: one row per team-season
- `player_seasons`: one row per player-team-season
- `transfers`: one row per school-to-school move, or derived from consecutive player seasons

### 2. Data cleaning and validation

- check shape, schema, data types, and season coverage
- standardize team/player text fields
- remove or investigate duplicate team-season and player-season records
- quantify missing values before imputation or exclusion
- verify unrealistic ranges rather than automatically deleting legitimate high performers
- create `Net Rating = Offensive Rating - Defensive Rating`
- validate joins across team, player, season, and transfer identifiers

### 3. Exploratory analysis

Key views include:

- Offensive Rating distribution
- Offensive Rating vs Defensive Rating
- Net Rating by season
- correlations among efficiency/style metrics
- pre-transfer vs post-transfer production
- transition summaries such as Low → High and Medium → High

### 4. Team profiling with K-means

Team profile features:

- Offensive Rating
- Defensive Rating
- Pace
- Effective Field Goal %
- Turnover %
- Offensive Rebound %
- Free Throw Rate
- Strength of Schedule

The features are standardized before K-means because clustering is distance-based. K-means creates three clusters. The clusters are then ordered by average Net Rating and labeled:

- **Low**
- **Medium**
- **High**

This is more defensible than manually assigning arbitrary ORtg/DRtg thresholds.

### 5. Transfer modeling table

Each historical transfer becomes one modeling row containing:

**Pre-transfer player features**
- minutes/game
- PPG
- Usage %
- True Shooting %
- Assist %
- Turnover %
- Rebound %
- Player Offensive Rating

**Source environment**
- source ORtg
- source DRtg
- source Net Rating
- source schedule strength
- source tier

**Destination environment**
- destination ORtg
- destination DRtg
- destination Net Rating
- destination schedule strength
- destination tier

**Transition**
- e.g. `Low → High`, `Medium → High`, `High → High`

**Observed post-transfer outcomes**
- post-transfer Player Offensive Rating
- post-transfer True Shooting %
- post-transfer PPG
- post-transfer Usage %

## Predictive models

The project intentionally compares model families covered in standard supervised-learning coursework:

### Linear Regression
Used as the interpretable baseline. It tests whether post-transfer outcomes can be explained reasonably well through approximately linear relationships.

### Decision Tree Regression
Adds interpretable nonlinear thresholds and interactions.

### Random Forest Regression
Combines many trees to capture more complex nonlinear relationships while reducing the instability of a single decision tree.

For each target, the models are evaluated on held-out data using:

- **MAE** — average absolute prediction error
- **R²** — proportion of target variation explained

The model with the lowest held-out MAE is selected for that target.

## KNN / comparable-player layer

Nearest-neighbor similarity is used as a staff-facing interpretation layer rather than only relying on one model prediction.

A candidate can be compared with historical transfers based on features such as:

- pre-transfer PPG
- pre-transfer Usage %
- pre-transfer TS%
- pre-transfer Player ORtg
- source team Net Rating / schedule strength
- destination team Net Rating / schedule strength

This supports outputs such as:

> “These are the historical transfers most statistically similar to this player, and this is how their production changed after transfer.”

## Why these models?

The project uses a simple progression:

`K-means team profiling → Linear Regression baseline → Decision Tree → Random Forest → KNN comparables`

This keeps the methodology understandable to non-technical stakeholders while still allowing nonlinear relationships and historical similarity analysis.

## Optional Phase 2: classification

A future extension could define a basketball-staff-approved outcome such as `successful high-major contributor: Yes/No` and compare:

- Logistic Regression
- KNN Classification
- Decision Tree Classification
- Random Forest Classification

That classification target should only be created after the staff defines what “success” means operationally.

## Validation recommendation for real historical data

A random train/test split is useful during prototyping, but a stronger sports-analytics validation design is:

> **Train on earlier seasons → test on the most recent season.**

This more closely matches the real recruiting use case: learn from historical transfers and project future outcomes.

## Decision-support output

A staff-facing result should prioritize a few actionable views:

1. Candidate player profile
2. Source team ORtg / DRtg / Net Rating / tier
3. Destination team ORtg / DRtg / Net Rating / tier
4. Projected post-transfer efficiency and role
5. Historical transition averages
6. Comparable historical transfers
7. Important model features
8. Model error / uncertainty and limitations

The model is intended to **support**, not replace, film review, coaching judgment, role/lineup fit, medical information, player development, and direct scouting.

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
└── README.md
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

## Moving from demo data to real historical data

Replace the demo CSV inputs with validated historical files using the documented schema. Keep the same analytics sequence:

`clean → validate → EDA → team profiling → transfers → feature engineering → model comparison → historical comparables → staff-facing visualization`

Do not present synthetic-data model metrics as real NCAA recruiting accuracy. Real basketball conclusions should only be reported after retraining and validating the pipeline on actual historical data.
