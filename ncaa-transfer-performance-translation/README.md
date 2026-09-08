# NCAA Transfer Performance Translation Model

A Python basketball analytics proof of concept for the question:

> **How might a player's performance translate when moving from one competitive team environment to another?**

The project is designed around a transfer-portal / recruiting workflow. It combines data cleaning, exploratory analysis, offensive/defensive team profiling, historical transfer analysis, comparable-player search, and predictive modeling.

> **Portfolio data note:** The repository includes deterministic synthetic NCAA-like demo data so the workflow can run end to end without redistributing licensed or proprietary data. The same pipeline is designed to accept real historical team, player-season, and transfer datasets when available.

## Analytics workflow

`clean & validate → EDA → K-means team profiles → transfer-level feature engineering → Linear Regression / Decision Tree / Random Forest → KNN comparables → staff-facing output`

## Selected analysis visuals

The views below reproduce the main Google Colab analyses used to develop and explain the workflow.

### Low / Medium / High team environment profiles

![Low Medium High team profiles](outputs/screenshots/team_environment_profiles.svg)

The team-season observations are grouped with K-means using offensive, defensive, pace, shooting, turnover, rebounding, free-throw and schedule-strength features. Cluster numbers are then ordered by average Net Rating and labeled Low, Medium and High.

### K-means elbow analysis

![K-means elbow method](outputs/screenshots/kmeans_elbow_method.svg)

The project uses three clusters because the basketball use case calls for Low / Medium / High environments, while the elbow view is used as a reasonableness check rather than choosing the number of clusters blindly.

## Business questions

1. What do team environments look like over multiple seasons?
2. Can teams be segmented into **Low / Medium / High** statistical profiles?
3. What historically happens when players move Low → High, Medium → High, High → High, etc.?
4. Which pre-transfer player and team-context features are most useful for explaining post-transfer performance?
5. Can historical data estimate post-transfer Offensive Rating, True Shooting %, PPG, and Usage %?
6. Which historical transfers are most similar to a current candidate?

## 1. Data ingestion

Expected real-world tables:

- `team_seasons`: one row per team-season
- `player_seasons`: one row per player-team-season
- `transfers`: one row per school-to-school move, or derived from consecutive player seasons

The included demo generator produces the same logical tables so the project can run without external data.

## 2. Data cleaning and validation

The workflow checks:

- shape, schema, data types, and season coverage
- duplicate team-season and transfer records
- missing values in modeling features
- standardized team text fields for joins
- `Net Rating = Offensive Rating - Defensive Rating`
- consistency across team, season, player, source-team and destination-team keys

Extreme basketball performances are not automatically deleted as outliers; they should first be checked for data-quality problems.

## 3. Exploratory data analysis

Key views include:

- Offensive Rating distribution
- Offensive Rating vs Defensive Rating
- Net Rating by season
- correlations among efficiency/style metrics
- player PPG distribution / outlier checks
- pre-transfer vs post-transfer production
- Low → High and Medium → High transition summaries

The reproducible chart script is `src/visualize_results.py`. Running the pipeline creates portfolio charts in `outputs/`.

## 4. Team profiling with K-means

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

This avoids manually assigning arbitrary ORtg/DRtg thresholds.

## 5. Transfer modeling table

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

## 6. Predictive models

The main regression models intentionally match models covered in supervised-learning coursework.

### Linear Regression
Used as the interpretable baseline. It tests whether post-transfer outcomes can be explained reasonably well through approximately linear relationships.

### Decision Tree Regression
Adds nonlinear threshold relationships and interactions while remaining relatively easy to explain.

### Random Forest Regression
Combines many trees to capture more complex relationships and reduce the instability of a single decision tree.

For each target, the models are compared using:

- **MAE** — average absolute prediction error; lower is better
- **R²** — proportion of target variation explained

The selected model is the one with the lowest test MAE.

## 7. Validation design

The current model code prefers a **time-based split**:

> train on earlier transfer seasons → test on the most recent destination season

This better represents the real recruiting use case than randomly mixing past and future seasons. A deterministic 75/25 fallback is used only when the available demo sample is too small for a reasonable latest-season test set.

## 8. KNN / comparable-player layer

Nearest-neighbor similarity is used as a staff-facing interpretation layer rather than relying only on one model prediction.

A candidate is compared with historical transfers using features such as:

- pre-transfer PPG
- pre-transfer Usage %
- pre-transfer TS%
- pre-transfer Player ORtg
- source team Net Rating / schedule strength
- destination team Net Rating / schedule strength

The dashboard can therefore show both a model projection and the most statistically similar historical transfer records.

## 9. Staff-facing Streamlit dashboard

`app/streamlit_app.py` lets a user:

- choose a destination team-season
- review destination ORtg, DRtg, Net Rating and tier
- enter a candidate's pre-transfer production
- enter source-team context
- project post-transfer ORtg, TS%, PPG and Usage%
- view the model selected for the primary target and its held-out error
- review five comparable historical transfers
- inspect aggregate historical transition results

The intent is decision support, not replacement of film, coaching judgment, role/lineup fit, availability, medical information or direct scouting.

## Optional Phase 2: classification

If basketball staff define an operational outcome such as `successful high-major contributor: Yes/No`, a later phase could compare:

- Logistic Regression
- KNN Classification
- Decision Tree Classification
- Random Forest Classification

The definition of "success" should come from staff rather than being invented solely for modeling convenience.

## Project structure

```text
ncaa-transfer-performance-translation/
├── app/
│   └── streamlit_app.py
├── data/
│   └── README.md
├── outputs/
│   ├── README.md
│   ├── model_metrics.json
│   ├── transition_summary.csv
│   └── screenshots/
│       ├── team_environment_profiles.svg
│       └── kmeans_elbow_method.svg
├── src/
│   ├── generate_demo_data.py
│   ├── build_model.py
│   ├── predict.py
│   └── visualize_results.py
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

Replace the generated demo CSVs with validated historical files using the documented schema. Keep the same sequence:

`clean → validate → EDA → team profiling → transfers → feature engineering → time-based model validation → historical comparables → staff-facing visualization`

Real basketball conclusions should only be reported after retraining and validating the pipeline on actual historical data.
