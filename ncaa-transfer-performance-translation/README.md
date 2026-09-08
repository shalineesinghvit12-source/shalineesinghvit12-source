# NCAA Transfer Performance Translation Model

A Python basketball analytics proof of concept built around one question:

> **How might a player's performance translate when moving from one competitive team environment to another?**

The project follows an end-to-end analytics workflow for a transfer-portal / recruiting use case:

`clean & validate → EDA → K-means team profiles → transfer feature engineering → Linear Regression / Decision Tree / Random Forest → KNN comparables → staff-facing output`

> **Data note:** The public repository uses deterministic synthetic NCAA-like demo data so the workflow can run end to end without redistributing licensed or proprietary data. The same pipeline is designed to accept validated historical team, player-season, and transfer data.

## What is implemented

This repository includes the full prototype workflow:

- data generation / ingestion structure for team-season, player-season, and transfer records
- data cleaning and validation checks
- exploratory data analysis and visualizations
- Low / Medium / High team-environment profiling with K-means
- transfer-level feature engineering using player, source-team, and destination-team context
- Linear Regression, Decision Tree Regression, and Random Forest Regression model comparison
- MAE and R² evaluation
- time-based validation logic using earlier seasons to predict the latest season when the sample size supports it
- KNN-style nearest-neighbor comparable-transfer analysis
- Streamlit decision-support dashboard
- transition summaries and portfolio visual outputs

## Google Colab analysis visuals

These views correspond to the exploratory analysis and team-profiling work completed in Google Colab.

### 1. Player PPG distribution / outlier check

<img width="408" height="252" alt="Points Per Game boxplot" src="https://github.com/user-attachments/assets/81936b60-8bef-4f21-948a-c6167c2c76eb" />

Used during data-quality review to understand the player scoring distribution and inspect extreme values rather than automatically removing high performers.

### 2. Offensive Rating distribution

<img width="490" height="305" alt="Offensive Rating distribution" src="https://github.com/user-attachments/assets/eae5aca3-4462-48b4-8f1e-276721948272" />

Shows the spread of team offensive efficiency across the five-season dataset.

### 3. Offensive vs Defensive Efficiency

<img width="492" height="339" alt="Team Offensive vs Defensive Efficiency" src="https://github.com/user-attachments/assets/2935db08-c540-4c74-b42f-2d393d15547d" />

This view helps explain overall team environments: stronger teams generally combine higher offensive efficiency with lower defensive rating.

### 4. Team efficiency across seasons

<img width="516" height="317" alt="Team Efficiency Across Seasons" src="https://github.com/user-attachments/assets/c3394cf2-3d9b-4f9b-b68c-ebfb5d80b0a1" />

Used to review whether average team efficiency shifts meaningfully by season before combining multiple years of data.

### 5. Team metric correlation matrix

<img width="413" height="331" alt="Team Metric Correlation Matrix" src="https://github.com/user-attachments/assets/f72c391d-ae21-4e1e-aff9-2da2e0b38704" />

Used to understand relationships among ORtg, DRtg, Net Rating, pace, shooting, turnover, rebounding, free-throw rate, and schedule strength.

### 6. K-means elbow analysis

<img width="408" height="264" alt="K-means elbow method" src="https://github.com/user-attachments/assets/8166e2f4-7282-40e9-a253-37e1f5002b04" />

The basketball use case calls for Low / Medium / High environments, so three clusters are used. The elbow view serves as a reasonableness check rather than choosing K blindly.

### 7. Low / Medium / High team environment profiles

<img width="458" height="314" alt="Low Medium High team profiles" src="https://github.com/user-attachments/assets/ab153c48-5595-451f-9ca6-70c437f01189" />

Team-season observations are standardized and grouped with K-means. The resulting clusters are ordered by average Net Rating and labeled **Low**, **Medium**, and **High**.

## Business questions

1. What do team environments look like over multiple seasons?
2. Can team-seasons be segmented into Low / Medium / High statistical profiles?
3. What historically happens when players move Low → High, Medium → High, High → High, and other transitions?
4. Which pre-transfer player and team-context features are most useful for explaining post-transfer performance?
5. Can historical data estimate post-transfer Offensive Rating, True Shooting %, PPG, and Usage %?
6. Which historical transfers are most statistically similar to a current candidate?

## Data used in a real-world version

The pipeline expects three logical tables:

- `team_seasons` — one row per team-season
- `player_seasons` — one row per player-team-season
- `transfers` — one row per school-to-school move, or derived from consecutive player seasons

The included demo generator produces the same logical structure. The recommended real-data schema is documented in `data/README.md`.

## Data cleaning and validation

Before modeling, the workflow:

- checks required columns and data types
- reviews season coverage
- removes duplicate team-season and duplicate transfer records
- standardizes team-name text used in joins
- checks missing values in team-profile and modeling features
- verifies source-team / destination-team keys
- calculates `Net Rating = Offensive Rating - Defensive Rating` when needed
- reviews percentage scales and unrealistic values before modeling
- treats extreme basketball performances as observations to investigate rather than automatically deleting them

For real historical data, player identifiers and team-name mappings should receive additional manual validation because transfer matching errors can create incorrect pre/post records.

## Exploratory data analysis

EDA is performed before clustering or prediction to understand distributions, relationships, season effects, and data-quality issues.

Core views include:

- PPG boxplot / outlier review
- Offensive Rating distribution
- Offensive Rating vs Defensive Rating
- average Net Rating across seasons
- team-metric correlation matrix
- K-means elbow analysis
- Low / Medium / High team-environment visualization
- pre-transfer vs post-transfer summaries by transition type

The reproducible portfolio plotting code is in `src/visualize_results.py`.

## Team profiling with K-means

Team profile features include:

- Offensive Rating
- Defensive Rating
- Pace
- Effective Field Goal %
- Turnover %
- Offensive Rebound %
- Free Throw Rate
- Strength of Schedule

Features are standardized with `StandardScaler` before K-means because clustering is distance-based. K-means creates three clusters, which are ordered by average Net Rating and mapped to Low / Medium / High.

The Low / Medium / High labels represent **statistical team environments**, not a claim that every team in a particular NCAA conference category is automatically Low, Medium, or High.

## Transfer feature engineering

Each historical transfer becomes one model row.

### Pre-transfer player features

- minutes/game
- PPG
- Usage %
- True Shooting %
- Assist %
- Turnover %
- Rebound %
- Player Offensive Rating

### Source-team context

- source Offensive Rating
- source Defensive Rating
- source Net Rating
- source Strength of Schedule
- source team tier

### Destination-team context

- destination Offensive Rating
- destination Defensive Rating
- destination Net Rating
- destination Strength of Schedule
- destination team tier

### Transition feature

Examples:

- `Low → High`
- `Medium → High`
- `High → High`

### Prediction targets

- post-transfer Player Offensive Rating
- post-transfer True Shooting %
- post-transfer PPG
- post-transfer Usage %

## Predictive models

The regression models intentionally match supervised-learning methods covered in coursework.

### Linear Regression

Used as an interpretable baseline to test whether post-transfer outcomes can be represented reasonably well through approximately linear relationships.

### Decision Tree Regression

Adds nonlinear threshold relationships and interactions while remaining relatively easy to explain.

### Random Forest Regression

Combines many decision trees to capture more complex relationships and reduce the instability of a single tree.

The project does **not** assume the most complex model is automatically best. The models are compared on unseen data, and the lowest test MAE is selected for each target.

## Model evaluation

Primary metrics:

- **MAE (Mean Absolute Error)** — average absolute prediction error; lower is better
- **R²** — proportion of outcome variation explained; higher is generally better

The committed `outputs/model_metrics.json` is a **synthetic-demo snapshot**, not evidence of real NCAA recruiting accuracy. Current demo results include Linear Regression as the selected model for Player ORtg, TS%, and Usage%, while Random Forest is selected for PPG. These results should be regenerated whenever the modeling code or input data changes.

## Validation design

The current modeling code prefers a time-based split:

> **train on earlier transfer seasons → test on the most recent destination season**

This more closely resembles the real recruiting workflow than randomly mixing past and future seasons. A deterministic 75/25 fallback is used only when the dataset is too small for a reasonable latest-season test set.

For a production historical-data version, the latest-season holdout should be preserved and model decisions should be made without using future-season outcomes during training.

## KNN comparable-player layer

Nearest-neighbor similarity is used as an interpretation layer rather than as the only prediction method.

A candidate is compared with historical transfers using features such as:

- pre-transfer PPG
- pre-transfer Usage %
- pre-transfer TS%
- pre-transfer Player ORtg
- source team Net Rating / schedule strength
- destination team Net Rating / schedule strength

This allows a staff member to see both a model projection and the most statistically similar historical transfer profiles and what happened after their moves.

## Historical transition analysis

The pipeline creates `outputs/transition_summary.csv`, summarizing pre/post changes by transition type. This supports questions such as:

- How did Low → High transfers perform after moving?
- How did Medium → High transfers change in PPG, TS%, or Player ORtg?
- Are High → High transfers more stable than larger jumps in environment?

This descriptive analysis is useful even before relying on a predictive model.

## Streamlit decision-support dashboard

`app/streamlit_app.py` allows a user to:

- choose a destination team-season
- review destination ORtg, DRtg, Net Rating, and tier
- enter a candidate's pre-transfer production
- enter source-team context
- project post-transfer ORtg, TS%, PPG, and Usage %
- view selected-model accuracy
- review five comparable transfer records
- inspect historical transition summaries

The model is intended to support — not replace — film review, coaching judgment, role/lineup fit, medical information, player development, and direct scouting.

## Optional Phase 2: classification

If basketball staff define an operational outcome such as `successful high-major contributor: Yes/No`, a later phase could compare:

- Logistic Regression
- KNN Classification
- Decision Tree Classification
- Random Forest Classification

The definition of success should come from staff rather than being invented solely for modeling convenience.

## Limitations and next steps

The current public version is a **methodology prototype**, not a validated NCAA recruiting model. A stronger real-world version should add:

- validated historical NCAA transfer records
- opponent-adjusted efficiency definitions from a consistent source
- conference / competition-level context kept separate from statistical team strength
- role and lineup context
- player class / experience / physical attributes when available
- coaching-system variables
- injury / availability information where appropriate and permitted
- uncertainty intervals around predictions
- additional out-of-time validation across multiple seasons

The most important next step is to retrain the same pipeline on the real historical datasets and compare whether the relationships observed in the demo persist.

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
│   └── transition_summary.csv
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

## Moving to real historical data

Replace the demo CSVs with validated historical files using the documented schema and keep the same sequence:

`clean → validate → EDA → team profiling → transfers → feature engineering → time-based validation → historical comparables → staff-facing visualization`

Real basketball conclusions should only be reported after retraining and validating the pipeline on actual historical data.
