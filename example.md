# F1 MCP Server — Example Prompts

Verified complex prompts that demonstrate multi-tool workflows against real race data.

---

## 1. Race Strategy Diagnosis

**Prompt:**
> Analyze why Verstappen won the 2023 Bahrain GP. Break down his tyre strategy, pit stops, race pace trend, and any overtakes he made.

**Tools triggered:**
- `get_driver_finish_position` — confirm race winner
- `get_tyre_strategy` — compound sequence and stint lengths
- `get_pit_stops` — pit stop laps and timing
- `get_pit_stop_time` — actual pit stop durations
- `performance_trend` — lap time evolution
- `get_overtakes` — position gains per lap
- `get_driver_race_progression` — position trace across race

---

## 2. Driver vs Teammate Deep Dive

**Prompt:**
> Compare Verstappen and Perez in the 2023 Bahrain GP race. Show their sector deltas, consistency scores, tyre degradation, and gap evolution throughout the race.

**Tools triggered:**
- `get_teammate` — confirm teammate pairing
- `sector_delta_vs_teammate` — per-sector time delta
- `driver_consistency_score` — lap time variance comparison
- `get_tyre_degradation_rate` — deg rate per compound
- `get_gap_to_leader` — gap to leader over laps
- `get_gap_between_drivers` — direct gap comparison

---

## 3. Pit Strategy Evaluation

**Prompt:**
> Evaluate whether Sainz could have beaten Perez at the 2023 Bahrain GP with different pit timing. Analyze undercut and overcut opportunities.

**Tools triggered:**
- `get_tyre_strategy` — strategies for both drivers
- `get_pit_stops` — pit laps comparison
- `undercut_effectiveness` — pace gain after early stops
- `overcut_effectiveness` — pace on extended stints
- `optimal_pit_window` — ideal pit window
- `get_pit_lane_loss` — time lost in pit lane

---

## 4. Tyre Degradation Intelligence

**Prompt:**
> Which driver managed tyre degradation best in the 2023 Bahrain GP? Show degradation rates by compound and predict tyre cliff timing.

**Tools triggered:**
- `get_tyre_degradation_rate` — deg slopes per driver/compound
- `predict_tyre_cliff` — predicted lap where performance drops
- `get_average_stint_length` — stint length comparison
- `get_stints` — stint details per driver
- `compare_tyre_performance` — compound-vs-compound analysis
- `generate_tyre_degradation_plot` — visual degradation curves

---

## 5. Telemetry Corner Analysis

**Prompt:**
> Compare Verstappen and Leclerc through Turn 10 at the 2023 Bahrain GP. Who brakes later, carries more apex speed, and gets on the throttle earlier?

**Tools triggered:**
- `corner_entry_speed` — speed approaching the corner
- `corner_apex_speed` — minimum speed through apex
- `corner_exit_speed` — acceleration out of corner
- `corner_speed_comparison` — side-by-side corner speeds
- `braking_point_analysis` — braking zone comparison
- `throttle_application_analysis` — throttle pickup timing

---

## 6. Battle Detection and Overtake Prediction

**Prompt:**
> Find the closest battles in the 2023 Bahrain GP and estimate the overtake probability between drivers who were within 1 second.

**Tools triggered:**
- `get_battle_detection` — find sub-1.5s gaps
- `predict_overtake_probability` — ML-based overtake likelihood
- `predict_battle_outcome` — predicted winner of each battle
- `get_position_changes` — net positions gained/lost
- `get_overtakes` — actual overtaking events

---

## 7. Driver Style Profiling

**Prompt:**
> Profile the driving styles in the 2023 Bahrain GP. Cluster drivers by aggression, consistency, and risk-taking behavior.

**Tools triggered:**
- `driver_aggression_index` — aggression score per driver
- `driver_consistency_score` — consistency score
- `driver_risk_index` — risk profile
- `driver_style_clustering` — ML clustering into archetypes
- `sector_consistency` — per-sector consistency

---

## 8. Safety Car and Race Neutralization Analysis

**Prompt:**
> Analyze the safety car and VSC periods in the 2023 Bahrain GP. What was the probability of a safety car and how did it affect the race?

**Tools triggered:**
- `get_safety_car_periods` — SC and VSC events with types
- `predict_safety_car_probability` — SC probability estimation
- `predict_virtual_safety_car_probability` — VSC probability
- `get_session_flag_events` — all flag events
- `get_track_status_changes` — status transition timeline

---

## 9. Race Simulation and What-If

**Prompt:**
> Simulate how the 2023 Bahrain GP would have played out if Verstappen used a two-stop strategy instead of his actual strategy.

**Tools triggered:**
- `get_tyre_strategy` — actual strategy used
- `race_strategy_simulation` — simulated outcomes
- `two_stop_vs_one_stop_simulation` — strategy comparison
- `predict_driver_position_end_of_race` — predicted finish position
- `predict_race_podium` — predicted podium with alternate strategy

---

## 10. Full Race Engineering Report

**Prompt:**
> Act as an F1 race engineer. Generate a complete technical race report for the 2023 Bahrain GP including:
> - Race result and winner prediction accuracy
> - Tyre strategy evaluation for all drivers
> - Pit stop efficiency analysis
> - Key overtakes and battles
> - Sector performance breakdown for top 5
> - Tyre degradation analysis by compound
> - Gap to leader evolution
> - Race pace trends
> - Generate speed map and race progression visualizations

**Tools triggered (20+):**
- `predict_race_winner`, `predict_race_podium` — predictions vs reality
- `get_driver_finish_position` — actual results
- `get_tyre_strategy`, `get_stints` — strategy overview
- `get_pit_stops`, `get_pit_stop_time`, `get_pit_lane_loss` — pit analysis
- `get_overtakes`, `get_battle_detection` — race action
- `get_best_sector_times`, `sector_performance_summary` — sector analysis
- `get_tyre_degradation_rate`, `compare_tyre_performance` — tyre analysis
- `get_gap_to_leader` — gap evolution
- `performance_trend` — pace trends
- `generate_speed_map`, `generate_race_progression_chart` — visualizations
