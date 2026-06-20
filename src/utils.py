from __future__ import annotations
from typing import Dict, List, Optional, Any
from psychopy import logging
import random
from psyflow.sim.rng import stable_int_hash

class RewardTracker:
    """Tracks cumulative reward across trials."""
    def __init__(self, initial_reward: int = 0):
        self.cumulative_reward = initial_reward

    def update(self, delta: int) -> int:
        self.cumulative_reward += int(delta)
        return self.cumulative_reward

def generate_bandit_schedule(
    block_idx: int,
    n_trials: int,
    seed: int,
    block_probabilities: list[dict[str, float]]
) -> list[tuple[float, float]]:
    """
    Generate a sequence of (p_left, p_right) for a block.
    """
    if not block_probabilities:
        return [(0.5, 0.5)] * n_trials
    
    row = block_probabilities[int(block_idx) % len(block_probabilities)]
    p_left = float(row.get("left", 0.5))
    p_right = float(row.get("right", 0.5))
    
    return [(p_left, p_right)] * int(n_trials)

def draw_bandit_reward(p_left: float, p_right: float, choice_side: str, rng: Optional[random.Random] = None) -> bool:
    """
    Stochastically draw a reward based on the chosen side.
    """
    p = float(p_left) if choice_side == "left" else float(p_right)
    p = max(0.0, min(1.0, p))
    if rng is None:
        raise ValueError("draw_bandit_reward requires a seeded rng")
    draw = rng.random()
    return draw < p

def get_fallback_choice(policy: str, left_key: str, right_key: str, rng: Optional[random.Random] = None) -> str:
    """
    Impute a choice in case of timeout.
    """
    policy = str(policy).lower().strip()
    if policy == "left":
        return left_key
    if policy == "right":
        return right_key
    
    if rng is None:
        raise ValueError("get_fallback_choice requires a seeded rng for random fallback")
    _rng = rng
    return left_key if _rng.random() < 0.5 else right_key


def make_trial_rng(settings: Any, trial_id: int, block_idx: int | None, salt: str) -> random.Random:
    base_seed = int(getattr(settings, "overall_seed", 0) or 0)
    rng_seed = stable_int_hash(base_seed, block_idx if block_idx is not None else 0, trial_id, salt)
    return random.Random(int(rng_seed))
