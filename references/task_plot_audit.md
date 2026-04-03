# Task Plot Audit

- generated_at: 2026-04-03T22:38:51
- mode: existing
- task_path: E:\Taskbeacon\T000038-two-armed-bandit

## 1. Inputs and provenance

- E:\Taskbeacon\T000038-two-armed-bandit\README.md
- E:\Taskbeacon\T000038-two-armed-bandit\config\config.yaml
- E:\Taskbeacon\T000038-two-armed-bandit\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Pre-choice fixation | Central fixation before choice. |
- | Bandit choice | Two options are displayed and response is captured (`F/J`). |
- | Choice confirmation | Selected option is highlighted briefly. |
- | Outcome feedback | Reward/no-reward feedback and running total are displayed. |
- | Inter-trial interval | Fixation before next trial. |

## 3. Evidence extracted from config/source

- bandit: phase=pre choice fixation, deadline_expr=duration, response_expr=n/a, stim_expr='fixation'
- bandit: phase=bandit choice, deadline_expr=decision_duration, response_expr=decision_duration, stim_expr='bandit_choice'
- bandit: phase=choice confirmation, deadline_expr=confirm_duration, response_expr=n/a, stim_expr='selection_confirmation'
- bandit: phase=outcome feedback, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=stim_id_fb
- bandit: phase=iti, deadline_expr=iti_duration, response_expr=n/a, stim_expr='fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.031, right=0.034, blank=0.124
  - layout pass 2: content-only rerender; plot copy translated to English for legibility
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0307, 'right_ratio': 0.0336, 'blank_ratio': 0.1245}
  - pass: 2
    note: manual content rewrite only; layout stayed stable after rerender

## 7. Output files and checksums

- E:\Taskbeacon\T000038-two-armed-bandit\references\task_plot_spec.yaml: sha256=1EF7A539EF94EA96D3DC6E73EDD052CC5D15442A34896DFEE91006A219DBF13C
- E:\Taskbeacon\T000038-two-armed-bandit\references\task_plot_spec.json: sha256=441CD27005860F523ADB9B4FECED32294FE33415C9F8A174E3872BD622DF0FF3
- E:\Taskbeacon\T000038-two-armed-bandit\references\task_plot_source_excerpt.md: sha256=03e7a4b4bc3577854d12b08fd9db2c6dee745c1b0bd29fbcebd30c2fe8dcaa20
- E:\Taskbeacon\T000038-two-armed-bandit\task_flow.png: sha256=17E6DEAA7841335B5B78366F3A18B3CF8C16E5EC024D58E662F6B71A67BFAB3D

## 8. Inferred/uncertain items

- bandit:pre choice fixation:heuristic numeric parse from 'float(getattr(settings, 'pre_choice_fixation_duration', 0.5))'
- bandit:bandit choice:heuristic numeric parse from 'float(getattr(settings, 'bandit_choice_duration', 2.5))'
- bandit:choice confirmation:heuristic numeric parse from 'float(getattr(settings, 'choice_confirmation_duration', 0.4))'
- bandit:outcome feedback:heuristic numeric parse from 'float(getattr(settings, 'outcome_feedback_duration', 0.8))'
- bandit:iti:heuristic numeric parse from 'float(getattr(settings, 'iti_duration', 0.6))'
- unparsed if-tests defaulted to condition-agnostic applicability: not choice_made
