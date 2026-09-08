# Data schema

The public repository does not commit licensed or proprietary NCAA datasets. `src/generate_demo_data.py` creates deterministic NCAA-like CSVs locally so the project can run end to end.

For a real historical version, place validated files in this folder using the same logical roles:

## team_seasons
One row per team-season. Recommended fields:

- `season`
- `team`
- `offensive_rating`
- `defensive_rating`
- `net_rating` (or compute ORtg - DRtg)
- `pace`
- `efg_pct`
- `turnover_pct`
- `off_rebound_pct`
- `free_throw_rate`
- `strength_of_schedule_z`

## player_seasons
One row per player-team-season. Recommended fields include player ID, season, team, position, minutes/game, PPG, Usage %, TS%, Assist %, Turnover %, Rebound %, and player Offensive Rating.

## transfers
One row per school-to-school move linking consecutive player seasons. The modeling pipeline expects pre-transfer player metrics, source-team context, destination-team context, and observed post-transfer outcomes.

Before modeling, validate team/player identifiers, season coverage, duplicates, missing values, percentage scales, and team-name consistency across files.
