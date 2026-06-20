from __future__ import annotations
from functools import partial
from psyflow import StimUnit, set_trial_context, next_trial_id
from .utils import draw_bandit_reward, get_fallback_choice, make_trial_rng

def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    reward_tracker, # RewardTracker
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one two-armed-bandit trial."""
    trial_id = next_trial_id()
    # condition is (p_left, p_right)
    p_left, p_right = float(condition[0]), float(condition[1])
    cond_id = f"L{int(round(p_left * 100)):02d}_R{int(round(p_right * 100)):02d}"
    
    trial_data = {
        "trial_id": trial_id,
        "condition": cond_id,
        "p_left": p_left,
        "p_right": p_right,
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    left_key = str(getattr(settings, "left_key", "f"))
    right_key = str(getattr(settings, "right_key", "j"))
    reward_win_val = int(getattr(settings, "reward_win", 10))
    reward_loss_val = int(getattr(settings, "reward_loss", 0))
    left_choice_label = str(getattr(stim_bank.get("machine_left_label"), "text", "左侧机器"))
    right_choice_label = str(getattr(stim_bank.get("machine_right_label"), "text", "右侧机器"))

    # Phase 1: pre_choice_fixation
    duration = float(getattr(settings, "pre_choice_fixation_duration", 0.5))
    cue = make_unit(unit_label="pre_choice_fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="pre_choice_fixation",
        deadline_s=duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"stage": "pre_choice_fixation", "block_idx": block_idx},
        stim_id="fixation",
    )
    cue.show(
        duration=duration,
        onset_trigger=settings.triggers.get("pre_choice_fixation_onset"),
    ).to_dict(trial_data)

    # Phase 2: bandit_choice (Fixed Duration)
    decision_duration = float(getattr(settings, "bandit_choice_duration", 2.5))
    choice = (
        make_unit(unit_label="bandit_choice")
        .add_stim(stim_bank.get("machine_left"))
        .add_stim(stim_bank.get("machine_right"))
        .add_stim(stim_bank.get("machine_left_label"))
        .add_stim(stim_bank.get("machine_right_label"))
        .add_stim(
            stim_bank.get_and_format(
                "choice_prompt",
                deadline_s=f"{decision_duration:.1f}",
            )
        )
    )

    set_trial_context(
        choice,
        trial_id=trial_id,
        phase="bandit_choice",
        deadline_s=decision_duration,
        valid_keys=[left_key, right_key],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={
            "stage": "bandit_choice",
            "p_left": p_left,
            "p_right": p_right,
            "block_idx": block_idx,
        },
        stim_id="bandit_choice",
    )

    choice.capture_response(
        keys=[left_key, right_key],
        correct_keys=[left_key, right_key],
        duration=decision_duration,
        onset_trigger=settings.triggers.get("bandit_choice_onset"),
        response_trigger={
            left_key: settings.triggers.get("bandit_choice_left_press"),
            right_key: settings.triggers.get("bandit_choice_right_press"),
        },
        timeout_trigger=settings.triggers.get("bandit_choice_no_response"),
    )

    resp_key = choice.get_state("response", None)
    choice_made = resp_key in (left_key, right_key)
    
    choice_forced = False
    if not choice_made:
        resp_key = get_fallback_choice(
            policy=getattr(settings, "no_choice_policy", "random"),
            left_key=left_key,
            right_key=right_key,
            rng=make_trial_rng(settings, trial_id, block_idx, "timeout_fallback"),
        )
        choice_forced = True
        trigger_runtime.send(settings.triggers.get("bandit_choice_forced"))

    side = "left" if resp_key == left_key else "right"
    rt = choice.get_state("rt", None)

    choice.set_state(
        choice_key=resp_key,
        choice_side=side,
        choice_made=choice_made,
        choice_forced=choice_forced,
    ).to_dict(trial_data)

    # Phase 3: choice_confirmation
    confirm_duration = float(getattr(settings, "choice_confirmation_duration", 0.4))
    choice_label = left_choice_label if side == "left" else right_choice_label
    highlight_id = "highlight_left" if side == "left" else "highlight_right"
    confirm = (
        make_unit(unit_label="choice_confirmation")
        .add_stim(stim_bank.get("machine_left"))
        .add_stim(stim_bank.get("machine_right"))
        .add_stim(stim_bank.get("machine_left_label"))
        .add_stim(stim_bank.get("machine_right_label"))
        .add_stim(stim_bank.get(highlight_id))
        .add_stim(stim_bank.get_and_format("target_prompt", choice_label=choice_label))
    )
    set_trial_context(
        confirm,
        trial_id=trial_id,
        phase="choice_confirmation",
        deadline_s=confirm_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"stage": "choice_confirmation", "choice_side": side, "block_idx": block_idx},
        stim_id="selection_confirmation",
    )
    confirm.show(
        duration=confirm_duration,
        onset_trigger=settings.triggers.get("choice_confirmation_onset"),
    ).to_dict(trial_data)

    # Phase 4: outcome_feedback
    win_outcome = draw_bandit_reward(
        p_left,
        p_right,
        side,
        rng=make_trial_rng(settings, trial_id, block_idx, "bandit_reward"),
    )
    delta = reward_win_val if win_outcome else reward_loss_val
    total = reward_tracker.update(delta)
    
    feedback_duration = float(getattr(settings, "outcome_feedback_duration", 0.8))
    stim_id_fb = "feedback_win" if win_outcome else "feedback_loss"
    feedback_stim = stim_bank.get_and_format(stim_id_fb, reward_delta=delta, total_score=total)
    
    feedback_trigger = settings.triggers.get("outcome_feedback_win_onset" if win_outcome else "outcome_feedback_loss_onset")
    
    feedback = make_unit(unit_label="outcome_feedback").add_stim(feedback_stim)
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="outcome_feedback",
        deadline_s=feedback_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"stage": "outcome_feedback", "reward_win": win_outcome, "block_idx": block_idx},
        stim_id=stim_id_fb,
    )
    feedback.show(
        duration=feedback_duration,
        onset_trigger=feedback_trigger,
    ).set_state(reward_win=win_outcome, reward_delta=delta, total_score=total).to_dict(trial_data)

    # Phase 5: iti
    iti_duration = float(getattr(settings, "iti_duration", 0.6))
    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=iti_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"stage": "iti", "block_idx": block_idx},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    # Canonical trial-level columns required by QA/trace contracts.
    trial_data.update(
        {
            "choice_key": resp_key,
            "choice_side": side,
            "choice_rt": rt,
            "reward_win": win_outcome,
            "reward_delta": delta,
            "total_score": total,
        }
    )

    return trial_data
