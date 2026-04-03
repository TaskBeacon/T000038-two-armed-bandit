# Two-Armed Bandit Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Two-Armed Bandit Task |
| Version | v0.2.3-dev |
| URL / Repository | https://github.com/TaskBeacon/T000038-two-armed-bandit |
| Short Description | Two-option bandit learning task with block-wise probability reversals. |
| Created By | TaskBeacon |
| Date Updated | 2026-04-03 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

This task implements a two-option bandit paradigm. On each trial, participants choose left or right, receive stochastic reward feedback, and update behavior across repeated trials. Reward probabilities are stable within a block and change across blocks to test learning and adaptation.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Parse mode/config | `main.py` loads runtime mode and YAML config. |
| 2. Initialize runtime | Window, keyboard, trigger runtime, stimulus bank, and task schedule settings are initialized. |
| 3. Prepare block schedule | Condition-generation settings prepare per-trial `(p_left, p_right)` schedule for the block. |
| 4. Execute trials | `BlockUnit(...).run_trial(...)` executes all planned trials. |
| 5. Block summary | Choice rates and reward metrics are displayed. |
| 6. Final summary | Final cumulative metrics are shown and data are saved. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Pre-choice fixation | Central fixation before choice. |
| Bandit choice | Two options are displayed and response is captured (`F/J`). |
| Choice confirmation | Selected option is highlighted briefly. |
| Outcome feedback | Reward/no-reward feedback and running total are displayed. |
| Inter-trial interval | Fixation before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Architecture note | No adaptive controller object is used; static condition-generation settings and task utilities drive scheduling/outcomes. |
| Block probabilities | Per-block left/right reward probabilities are configured. |
| Reward sampling | Bernoulli draw from selected-side probability. |
| No-response fallback | Optional policy imputes a choice when no response is made. |
| State tracking | `RewardTracker` tracks cumulative reward. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `pre_choice_fixation` | Fixation stage before choice. |
| `bandit_choice` | Choice response window. |
| `choice_confirmation` | Selected-option confirmation stage. |
| `outcome_feedback` | Trial outcome feedback stage. |
| `iti` | ITI stage. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `black` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `fixation` | text | Central fixation marker. |
| `machine_left/right` | rect | Left/right option panels. |
| `machine_left_label/right_label` | text | Option labels. |
| `highlight_left/right` | rect | Selected option highlight. |
| `choice_prompt` | text | Choice prompt with response deadline. |
| `target_prompt` | text | Choice confirmation text. |
| `feedback_win/loss` | text | Reward outcome feedback. |
| `block_break` / `good_bye` | text | Block/final summary pages. |

### d. Timing

| Phase | Duration |
|---|---|
| pre_choice_fixation_duration | 0.5 s |
| bandit_choice_duration | 2.5 s |
| choice_confirmation_duration | 0.4 s |
| outcome_feedback_duration | 0.8 s |
| iti_duration | 0.6 s |

## 4. Methods (for academic publication)

Participants repeatedly chose between two bandit options under uncertain reward contingencies. Choice was followed by explicit selection confirmation and immediate reward/no-reward feedback. This design supports estimation of trial-wise value learning and choice bias.

Reward probabilities were manipulated at the block level. Within each block, option probabilities remained fixed; across blocks, probabilities changed to induce strategy adaptation. Core outcomes include side choice proportions, reward rate, cumulative score, and response timing.

The implementation supports `human`, `qa`, and `sim` modes under a shared trial pipeline with standardized context instrumentation.
