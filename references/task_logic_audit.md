# Task Logic Audit: Two-Armed Bandit

## 1. Paradigm Intent

- Task: `two_armed_bandit`
- Primary construct: reinforcement learning under probabilistic outcomes with repeated binary choice.
- Manipulated factors: block-level reward contingencies (`p_left`, `p_right`) and contingency reversals across blocks.
- Dependent measures: choice side, response time, forced-choice incidence on timeout, reward outcome, cumulative score.
- Key citations:
  - `DAW2006_NATURE`
  - `WILSON2014_JEPG`
  - `SCHULZ2019_PNAS`

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: `task.total_blocks` (`4` in human profile; `1` in QA/sim smoke profiles).
- Trials per block: `task.trial_per_block` (`40` in human profile; `12` in QA/sim).
- Randomization/counterbalancing:
  - `generate_bandit_schedule(...)` expands block-level probability schedules into per-trial `(p_left, p_right)` tuples.
  - `randomize_within_block=false` preserves schedule order.
  - Block seed offset keeps deterministic reproducibility per block.

### Trial State Machine

1. `pre_choice_fixation`
   - Onset trigger: `pre_choice_fixation_onset` (`20`).
   - Stimuli shown: central fixation (`fixation`).
   - Valid keys: none.
   - Timeout behavior: auto-advance after `timing.pre_choice_fixation_duration`.
   - Next state: `bandit_choice`.
2. `bandit_choice`
   - Onset trigger: `bandit_choice_onset` (`30`).
   - Response triggers: `bandit_choice_left_press` (`31`) and `bandit_choice_right_press` (`32`).
   - Timeout trigger: `bandit_choice_no_response` (`33`).
   - Forced-choice marker on no response: `bandit_choice_forced` (`34`).
   - Stimuli shown: left/right machine panels with labels and choice prompt.
   - Valid keys: `[left_key, right_key]` (`f`, `j`).
   - Timeout behavior: if no response, task no-response policy imputes side using `no_choice_policy`.
   - Next state: `choice_confirmation`.
3. `choice_confirmation`
   - Onset trigger: `choice_confirmation_onset` (`40`).
   - Stimuli shown: same option panels + selected highlight + confirmation text.
   - Valid keys: none.
   - Timeout behavior: auto-advance after `timing.choice_confirmation_duration`.
   - Next state: `outcome_feedback`.
4. `outcome_feedback`
   - Onset trigger: `outcome_feedback_win_onset` (`50`) or `outcome_feedback_loss_onset` (`51`).
   - Stimuli shown: win/loss feedback with updated cumulative score.
   - Valid keys: none.
   - Timeout behavior: auto-advance after `timing.outcome_feedback_duration`.
   - Next state: `iti`.
5. `iti`
   - Onset trigger: `iti_onset` (`60`).
   - Stimuli shown: central fixation.
   - Valid keys: none.
   - Timeout behavior: auto-advance after `timing.iti_duration`.
   - Next state: next trial or block-end summary.

## 3. Condition Semantics

- Condition token in config: `bandit`.
- Participant-facing meaning: each trial presents two side-by-side machines; participant chooses one to maximize total reward.
- Runtime condition realization:
  - Effective condition ID is trial-specific probability signature (for example `L75_R25`) generated from the condition schedule.
  - Each trial carries `p_left` and `p_right`, used for stochastic reward sampling on chosen side.

## 4. Response and Scoring Rules

- Response mapping:
  - `f` -> left machine
  - `j` -> right machine
- Missing-response policy:
  - If no key in `bandit_choice` deadline, no-response policy imputes a choice (`no_choice_policy`).
  - Trial is marked `choice_forced=true` and `bandit_choice_forced` trigger is emitted.
- Correctness logic:
  - No objective correct side; both keys are valid actions under uncertainty.
- Reward update:
  - Bernoulli reward draw from chosen-side probability.
  - Reward delta: `reward_win` (default `10`) on win, `reward_loss` (default `0`) on loss.
  - `RewardTracker` updates cumulative score after each trial.
- Logged outputs:
  - `choice_key`, `choice_side`, `choice_rt`, `choice_forced`
  - `p_left`, `p_right`, `choice_prob`
  - `reward_win`, `reward_delta`, `total_score`

## 5. Stimulus Layout Plan

- Screen: `bandit_choice`
  - Stimulus IDs shown: `machine_left`, `machine_right`, `machine_left_label`, `machine_right_label`, `choice_prompt`
  - Layout anchors: left option at `[-230, 20]`, right option at `[230, 20]`, prompt at `[0, -210]`
  - Size/spacing: machine cards `240x300`, highlight frames `270x330`, center-to-center separation `460`
  - Readability checks: labels centered within cards, prompt below card row with clear vertical separation
  - Rationale: symmetric binary layout avoids implicit side bias and matches canonical two-option bandit display
- Screen: `choice_confirmation`
  - Stimulus IDs shown: all choice-screen elements + selected `highlight_left/right` + `target_prompt`
  - Layout anchors: highlight overlays card position; confirmation text at `[0, 210]`
  - Size/spacing: confirmation text height `36`, wrap width `980`
  - Readability checks: confirmation text does not overlap cards/labels
  - Rationale: brief explicit confirmation separates motor response from feedback onset for cleaner event timing

## 6. Trigger Plan

- Experiment:
  - `exp_onset` = 1
  - `exp_end` = 2
- Block:
  - `block_onset` = 10
  - `block_end` = 11
- Trial:
  - `pre_choice_fixation` onset -> `pre_choice_fixation_onset` = 20
  - `bandit_choice` onset -> `bandit_choice_onset` = 30
  - `bandit_choice` responses -> `bandit_choice_left_press` = 31 / `bandit_choice_right_press` = 32
  - `bandit_choice` timeout -> `bandit_choice_no_response` = 33
  - `bandit_choice` imputation marker -> `bandit_choice_forced` = 34
  - `choice_confirmation` onset -> `choice_confirmation_onset` = 40
  - `outcome_feedback` onset -> `outcome_feedback_win_onset` = 50 / `outcome_feedback_loss_onset` = 51
  - `iti` onset -> `iti_onset` = 60

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style (simple single flow / helper-heavy / why):
  - simple mode-aware flow with direct block loop and explicit phase logging.
- `utils.py` used? (yes/no)
  - yes.
- If yes, exact purpose (adaptive controller / sequence generation / asset pool / other):
  - sequence generation, reward sampling, and task-specific fallback choice helpers.
- Custom controller used? (yes/no)
  - no.
- If yes, why PsyFlow-native path is insufficient:
  - n/a; the task uses PsyFlow-native block scheduling plus lightweight helpers.
- Legacy/backward-compatibility fallback logic required? (yes/no)
  - no.
- If yes, scope and removal plan:
  - not applicable.

## 8. Inference Log

- Decision: keep explicit `choice_confirmation` stage between response and feedback.
  - Why inference was required: core papers specify choice and outcome events but not a mandatory visual confirmation epoch.
  - Citation-supported rationale: improves event separability for behavior/EEG timing while preserving reinforcement-learning structure.
- Decision: use discrete score mapping (`+10` win / `+0` loss).
  - Why inference was required: literature reports reward contingencies but not a unique UI scoring format.
  - Citation-supported rationale: simple deterministic scoring is faithful to binary outcome structure and supports participant comprehension.
