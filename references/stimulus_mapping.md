# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `bandit` | `pre_choice_fixation` | `fixation` | Central fixation before choice presentation | DAW2006_NATURE | Standard trial pacing before decision epoch | psychopy_builtin | config text stimulus | Neutral pre-choice stage |
| `bandit` | `bandit_choice` | `machine_left`, `machine_right`, `machine_left_label`, `machine_right_label`, `choice_prompt` | Two side-by-side options with left/right response mapping prompt | DAW2006_NATURE; WILSON2014_JEPG | Repeated binary choices in explore/exploit paradigm | psychopy_builtin | config shape/text stimuli | No raw condition labels shown |
| `bandit` | `choice_confirmation` | `highlight_left`, `highlight_right`, `target_prompt` | Brief confirmation of selected option | inferred | Separates motor response from outcome feedback onset | psychopy_builtin | config shape/text stimuli | Only selected side is highlighted |
| `bandit` | `outcome_feedback` | `feedback_win`, `feedback_loss` | Win/loss feedback with score update | DAW2006_NATURE; SCHULZ2019_PNAS | Stochastic reward outcome after each choice | psychopy_builtin | config text stimuli | Valence-specific feedback |
| `bandit` | `iti` | `fixation` | Inter-trial fixation | DAW2006_NATURE | Standard ITI event separation | psychopy_builtin | config text stimulus | Shared phase stimulus |
| `all` | `instruction/block_break/goodbye` | `instruction_text`, `block_break`, `good_bye` | Task instructions and summary/break pages | inferred | Operational task control screens | psychopy_builtin | config text stimuli | Localization-ready config text |
