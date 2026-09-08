# Demo data and real-world schema

The public repository now starts from **pre-generated synthetic NCAA-like demo data**. The purpose is to make the analytics workflow reproducible without distributing licensed, proprietary, or scraped NCAA data.

## Committed demo inputs

- `team_seasons_demo.csv` — 60 team-season rows covering 12 fictional programs from 2021–2025.
- `transfers_demo.csv` — 60 synthetic transfer records containing pre-transfer production, source/destination team context, and observed post-transfer outcomes.
- `player_seasons_demo.csv.gz` — compressed player-season source table used to demonstrate the player-level schema and EDA.

These files are the **starting point** of the public pipeline. No data-generation step is required when running the project.

## Team-season schema

One row per team-season. Important fields include:

- `season`
- `team`
- `offensive_rating`
- `defensive_rating`
- `net_rating`
- `pace`
- `efg_pct`
- `turnover_pct`
- `off_rebound_pct`
- `free_throw_rate`
- `strength_of_schedule_z`

## Player-season schema

One row per player-team-season. Important fields include player ID, player name, season, team, position, minutes/game, PPG, Usage %, TS%, Assist %, Turnover %, Rebound %, and Player Offensive Rating.

## Transfer modeling schema

One row per school-to-school move. Each row contains:

- player identity and position
- source and destination seasons/teams
- pre-transfer player production
- source-team ORtg, DRtg, Net Rating, and schedule-strength context
- destination-team ORtg, DRtg, Net Rating, and schedule-strength context
- observed post-transfer PPG, Usage %, TS%, and Player ORtg

## Using real historical data

In a production version, replace the demo files with validated historical team, player-season, and transfer data that follow the same logical schema. Before modeling, validate identifiers, season coverage, duplicates, missing values, percentage scales, team-name consistency, and source/destination joins.
