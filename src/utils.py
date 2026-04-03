from __future__ import annotations
from typing import Dict, List, Optional, Any
from psychopy import logging
import random

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
    draw = rng.random() if rng else random.random()
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
    
    _rng = rng or random.Random()
    return left_key if _rng.random() < 0.5 else right_key
