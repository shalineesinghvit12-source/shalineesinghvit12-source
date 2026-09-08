# NCAA Transfer Performance Translation Model

A Python basketball analytics proof of concept built around one question:

> **How might a player's performance translate when moving from one competitive team environment to another?**

The project is designed for a transfer-portal / recruiting decision-support workflow and follows this end-to-end analytics sequence:

`pre-generated demo data → cleaning & validation → EDA → K-means team profiles → transfer feature engineering → predictive model comparison → KNN comparables → staff-facing dashboard`

> **Data note:** The public repository uses synthetic NCAA-like demo data so the project can be shared and run without distributing licensed or proprietary NCAA data. The same workflow is designed to be retrained on validated historical team, player-season, and transfer data.

## Why this project is useful

Raw production such as 17 PPG does not mean the same thing in every environment. A transfer may face a different level of team efficiency, defensive quality, schedule strength, pace, role, and usage after changing schools.

This prototype combines the player's **pre-transfer production** with the **source-team environment** and **destination-team environment** to support questions such as:

- What type of team environment is the player leaving?
- What type of environment is he entering?
- How have similar Low → High, Medium → High, or other transfers changed historically?
- What post-transfer ORtg, TS%, PPG, or Usage% does the model project?
- Which historical transfer profiles are most similar to the candidate?
- Which inputs appear most important to the prediction?

The output is intended to add quantitative context to scouting and recruiting discussions, not replace film, coaching judgment, role fit, medical information, or direct player evaluation.

## Demo data included in the repository

The repository starts from committed demo inputs in `data/`; there is **no data-generation step required**.

- `team_seasons_demo.csv` — 60 team-season records for 12 fictional programs across 2021–2025
- `transfers_demo.csv` — 60 synthetic transfer records with pre-transfer, source-team, destination-team, and post-transfer fields
- `player_seasons_demo.csv.gz` — compressed player-season data used for player-level EDA and schema demonstration

A real-world version would replace these files with validated historical data while keeping the same pipeline structure.

## What is implemented

- committed demo input data
- explicit data-cleaning and validation stage
- exploratory data analysis and reproducible charts
- K-means Low / Medium / High team-environment profiling
- transfer-level feature engineering
- Linear Regression, Decision Tree Regression, and Random Forest Regression comparison
- MAE and R² evaluation
- time-based validation using earlier seasons to predict 2025 in the committed demo
- KNN-style comparable-transfer search
- historical transition analysis
- model feature-importance visualization
- Streamlit decision-support dashboard

# 1. Data cleaning and validation

`src/clean_data.py` is the first pipeline step.

It checks and prepares the demo inputs by:

- verifying required columns
- standardizing team and position text
- removing duplicate team-season, player-season, and transfer records
- checking missing values in required fields
- creating Net Rating when needed
- sorting records consistently by season / player
- producing a `data_quality_summary.csv`

Cleaned outputs are written to `outputs/`:

- `team_seasons_clean.csv`
- `player_seasons_clean.csv`
- `transfers_clean.csv`

A legitimate high-performing basketball player is not automatically deleted as an outlier. Extreme values should first be checked for data-quality issues.

# 2. Exploratory data analysis (EDA)

`src/eda.py` generates reproducible EDA charts before modeling.

The analysis includes:

- Player PPG boxplot / outlier review
- Offensive Rating distribution
- Offensive Rating vs Defensive Rating
- average Net Rating by season
- team-metric correlation matrix
- pre-transfer vs post-transfer PPG

These checks help answer whether the data is reasonable, how team efficiency is distributed, whether seasons differ, and which variables are related before clustering or prediction.

## Google Colab analysis visuals

### Player PPG distribution / outlier check

<img width="408" height="252" alt="Points Per Game boxplot" src="https://github.com/user-attachments/assets/81936b60-8bef-4f21-948a-c6167c2c76eb" />

### Offensive Rating distribution

<img width="490" height="305" alt="Offensive Rating distribution" src="https://github.com/user-attachments/assets/eae5aca3-4462-48b4-8f1e-276721948272" />

### Offensive vs Defensive Efficiency

<img width="492" height="339" alt="Team Offensive vs Defensive Efficiency" src="https://github.com/user-attachments/assets/2935db08-c540-4c74-b42f-2d393d15547d" />

### Team efficiency across seasons

<img width="516" height="317" alt="Team Efficiency Across Seasons" src="https://github.com/user-attachments/assets/c3394cf2-3d9b-4f9b-b68c-ebfb5d80b0a1" />

### Team metric correlation matrix

<img width="413" height="331" alt="Team Metric Correlation Matrix" src="https://github.com/user-attachments/assets/f72c391d-ae21-4e1e-aff9-2da2e0b38704" />

# 3. Team profiling with K-means

The team-profile features are:

- Offensive Rating
- Defensive Rating
- Pace
- Effective Field Goal %
- Turnover %
- Offensive Rebound %
- Free Throw Rate
- Strength of Schedule

The variables are standardized with `StandardScaler` because K-means is distance-based.

K-means then creates three statistical team environments. The raw cluster IDs are ordered by average Net Rating and labeled:

- **Low**
- **Medium**
- **High**

These labels describe **statistical team environments** in the prototype. They should not be interpreted as an automatic conference-level or low-major / high-major classification.

### K-means elbow analysis

<img width="408" height="264" alt="K-means elbow method" src="https://github.com/user-attachments/assets/8166e2f4-7282-40e9-a253-37e1f5002b04" />

Three clusters match the Low / Medium / High business use case; the elbow view is used as a reasonableness check rather than choosing K blindly.

### Low / Medium / High team environment profiles

<img width="458" height="314" alt="Low Medium High team profiles" src="https://github.com/user-attachments/assets/ab153c48-5595-451f-9ca6-70c437f01189" />

# 4. Transfer feature engineering

Each transfer becomes one modeling row.

## Pre-transfer player features

- Minutes/game
- PPG
- Usage %
- True Shooting %
- Assist %
- Turnover %
- Rebound %
- Player Offensive Rating

## Source-team context

- source Offensive Rating
- source Defensive Rating
- source Net Rating
- source Strength of Schedule
- source team tier

## Destination-team context

- destination Offensive Rating
- destination Defensive Rating
- destination Net Rating
- destination Strength of Schedule
- destination team tier

## Transition feature

Examples:

- `Low → High`
- `Medium → High`
- `High → High`
- `Medium → Low`

## Prediction targets

The prototype predicts four continuous outcomes:

- post-transfer Player Offensive Rating
- post-transfer True Shooting %
- post-transfer PPG
- post-transfer Usage %

# 5. Predictive models used

The project intentionally uses models that are straightforward to explain and compare.

## Linear Regression

Used as the interpretable baseline. It tests whether the relationship between pre-transfer production, team context, and the post-transfer outcome can be represented approximately linearly.

## Decision Tree Regression

Adds nonlinear threshold relationships. For example, a player's translation may change after certain combinations of pre-transfer efficiency, usage, or destination-team strength.

## Random Forest Regression

Combines many decision trees. It can capture more complex interactions while reducing the instability of a single tree.

The project does **not** assume Random Forest should win because it is more complex. All three models are evaluated on unseen data and the lowest-MAE model is selected for each target.

# 6. Model evaluation and validation

The primary evaluation metrics are:

- **MAE (Mean Absolute Error)** — average absolute prediction error; lower is better
- **R²** — proportion of outcome variation explained; higher is generally better

The committed demo uses a **time-based validation design**:

> **train on transfers ending before 2025 → test on 2025 transfers**

This more closely reflects the real recruiting use case than mixing future and past observations randomly.

## Current synthetic-demo model results

| Target | Selected model | MAE | R² |
|---|---|---:|---:|
| Player ORtg | Random Forest | 3.178 | 0.716 |
| True Shooting % | Random Forest | 1.908 | 0.585 |
| PPG | Random Forest | 3.962 | 0.463 |
| Usage % | Random Forest | 2.327 | 0.659 |

These numbers are **demonstration results from synthetic data**, not evidence of validated NCAA recruiting accuracy.

# 7. Historical transition analysis

`outputs/transition_summary.csv` summarizes how player production changes by environment transition.

Examples of questions this supports:

- How did Low → High players change in PPG, TS%, or ORtg?
- How did Medium → High players translate?
- Are High → High moves more stable?
- Which transition types have the largest historical drop or increase?

This descriptive layer is valuable even before using a predictive model because it gives staff a historical reference point.

# 8. KNN-style comparable-player analysis

The project uses nearest-neighbor similarity to find transfer profiles that are statistically close to a candidate.

Similarity features include:

- pre-transfer PPG
- pre-transfer Usage %
- pre-transfer TS%
- pre-transfer Player ORtg
- source team Net Rating / schedule strength
- destination team Net Rating / schedule strength

This makes a prediction easier to interpret. Instead of only saying:

> "Projected ORtg = 108"

staff can also see:

> "These are the five most statistically similar transfer profiles, and this is what happened after they moved."

# 9. How the project supports basketball decision making

The project is designed as a **decision-support tool**, not an automatic recruiting decision engine.

For a candidate transfer, the workflow can provide:

1. **Player context** — pre-transfer PPG, Usage, TS%, ORtg, minutes, assists, turnovers, and rebounding.
2. **Source environment** — where the production was created: ORtg, DRtg, Net Rating, schedule strength, and Low / Medium / High profile.
3. **Destination environment** — how different the new team context is.
4. **Historical translation** — what happened to players making similar environment changes.
5. **Model projection** — expected post-transfer ORtg, TS%, PPG, and Usage%.
6. **Comparable transfers** — historically similar player/team-context combinations.
7. **Model uncertainty context** — MAE and R² so staff can see how much error exists in the model.
8. **Feature importance** — which inputs the Random Forest relies on most strongly as an additional diagnostic view.

The goal is to help staff ask better questions, such as whether a player's production is likely to hold when the competition and role change, and which historical examples deserve a closer film review.

# 10. Streamlit decision-support dashboard

`app/streamlit_app.py` allows a user to:

- choose a destination team-season
- view destination ORtg, DRtg, Net Rating, and tier
- enter a candidate's pre-transfer statistics
- enter source-team context
- project post-transfer ORtg, TS%, PPG, and Usage%
- view the selected model and its error
- review five comparable transfers
- inspect historical transition summaries

# Optional Phase 2: classification

If basketball staff define an operational outcome such as `successful high-major contributor: Yes/No`, a later phase could compare:

- Logistic Regression
- KNN Classification
- Decision Tree Classification
- Random Forest Classification

The definition of success should come from basketball staff rather than being invented only for modeling convenience.

# Limitations and next steps

The current public project is a methodology prototype. A production version should add:

- validated historical NCAA team and transfer data
- a consistent opponent-adjusted efficiency source
- conference / competition level kept separate from statistical team strength
- role and lineup context
- player class, experience, height, or other available attributes
- coaching-system variables
- injury / availability context where appropriate and permitted
- uncertainty intervals
- additional out-of-time validation across multiple seasons

The most important next step is to replace the demo files with real historical data and determine whether the relationships observed in the prototype persist.

# Project structure

```text
ncaa-transfer-performance-translation/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── README.md
│   ├── team_seasons_demo.csv
│   ├── transfers_demo.csv
│   └── player_seasons_demo.csv.gz
├── outputs/
│   ├── README.md
│   ├── model_metrics.json
│   ├── transition_summary.csv
│   └── screenshots/
├── src/
│   ├── clean_data.py
│   ├── eda.py
│   ├── build_model.py
│   ├── predict.py
│   └── visualize_results.py
├── run_pipeline.py
├── requirements.txt
└── README.md
```

# Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py
streamlit run app/streamlit_app.py
```

The pipeline starts from the committed files in `data/` and runs:

`clean data → EDA → team profiling → transfer feature engineering → model comparison → transition analysis → portfolio charts`

# Moving to real historical data

Replace the demo inputs with validated historical files that follow the schema documented in `data/README.md`, then run the same analytical sequence.

Real basketball conclusions should only be reported after retraining and validating the pipeline on actual historical data.
