# CHANGELOG

All notable development changes for `T000038-two-armed-bandit` are documented here.

## [Unreleased]

### Changed
- Refactored `src/utils.py`: Removed adaptive RT logic; introduced `RewardTracker` for separate scoring logic and moved static schedule generation to `generate_bandit_schedule`.
- Refactored `src/run_trial.py` to contain logic for a single trial with fixed durations, aligned with `task_logic_audit.md`.
- Updated `main.py` to use `RewardTracker` and fixed-period trial flow.
- Removed unnecessary top-level `controller` config usage in favor of `condition_generation` settings and explicit `no_choice_policy` wiring in `main.py`.
- Renamed internal `StimUnit` labels in `src/run_trial.py` to match actual task phases (`pre_choice_fixation`, `bandit_choice`, `choice_confirmation`, `outcome_feedback`).

## [0.2.1-dev] - 2026-02-19

### Changed
- Refactored `src/run_trial.py` to remove template-style unit labels (`cue`, `anticipation`, `target`, `feedback`) in favor of paradigm-specific labels:
  - `pre_choice_fixation`, `bandit_choice`, `choice_confirmation`, `outcome_feedback`, `iti`.
- Migrated canonical timing keys in all configs:
  - `cue_duration` -> `pre_choice_fixation_duration`
  - `anticipation_duration` -> `bandit_choice_duration`
  - `target_duration` -> `choice_confirmation_duration`
  - `feedback_duration` -> `outcome_feedback_duration`
- Migrated canonical trigger keys in all configs:
  - `cue_onset` -> `pre_choice_fixation_onset`
  - `choice_onset` -> `bandit_choice_onset`
  - `choice_left_press/right_press/no_response/forced` -> `bandit_choice_left_press/right_press/no_response/forced`
  - `target_onset` -> `choice_confirmation_onset`
  - `feedback_win_onset/feedback_loss_onset` -> `outcome_feedback_win_onset/outcome_feedback_loss_onset`
- Replaced template `references/task_logic_audit.md` with a task-specific manual logic audit aligned to implemented state machine and triggers.
- Updated `references/parameter_mapping.md`, `references/stimulus_mapping.md`, and `README.md` for naming consistency and audit-to-code traceability.

### Fixed
- Standardized ITI phase/state naming to `iti` instead of `inter_trial_interval` in runtime metadata.
- Added backward-compatible lookup in `run_trial.py` for legacy timing/trigger keys to avoid breaking older configs.
- Fixed `block_break` formatting crash by providing `accuracy` in `main.py` block summary rendering.
- Fixed `responders/task_sampler.py` phase routing to use `bandit_choice` (with legacy `anticipation` fallback) so sampler decisions are applied at the actual choice phase.

## [0.2.0] - 2026-02-17

### Changed
- Replaced MID-style placeholder implementation with a real two-armed-bandit trial flow:
  - choice between left/right machines
  - probabilistic reward draw based on selected machine
  - selection confirmation stage
  - reward/score feedback with cumulative scoring
- Replaced adaptive target-duration controller with block probability schedule controller (`src/utils.py`).
- Refactored `main.py` to generate per-block probability conditions via controller and report bandit metrics (left choice rate, win rate, score).
- Rewrote configs to human-friendly, mode-separated profiles with Chinese participant text and `SimHei` font:
  - `config.yaml`
  - `config_qa.yaml`
  - `config_scripted_sim.yaml`
  - `config_sampler_sim.yaml`
- Replaced generic sampler with task-specific bandit sampler policy in `responders/task_sampler.py`.
- Updated `README.md` to standardized task2doc contract sections and two-armed-bandit logic.

### Fixed
- Removed non-bandit cue/target hit-miss logic inherited from MID scaffold.
- Removed condition labels shown as participant-facing protocol cues.

### Verified
- `python -m psyflow.validate <task_path>`
- `python main.py qa --config config/config_qa.yaml`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Two-Armed Bandit Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
