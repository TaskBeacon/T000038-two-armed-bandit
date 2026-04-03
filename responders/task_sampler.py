from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import math

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Task-specific sampler for two-armed-bandit choices."""

    left_key: str = "f"
    right_key: str = "j"
    inverse_temp: float = 6.0
    exploration: float = 0.05
    bias_left: float = 0.0
    rt_mean_s: float = 0.45
    rt_sd_s: float = 0.08
    rt_min_s: float = 0.15

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.inverse_temp = max(0.01, float(self.inverse_temp))
        self.exploration = max(0.0, min(1.0, float(self.exploration)))
        self.bias_left = float(self.bias_left)
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def end_session(self) -> None:
        self._rng = None

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def _normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return 0.5

    @staticmethod
    def _clip_prob(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "bandit_sampler", "reason": "no_valid_keys"})

        rng = self._rng
        if rng is None:
            return Action(key=None, rt_s=None, meta={"source": "bandit_sampler", "reason": "rng_missing"})

        rt = max(self.rt_min_s, self._normal(self.rt_mean_s, self.rt_sd_s))
        factors = dict(obs.task_factors or {})
        phase = str(obs.phase or factors.get("stage") or "").strip().lower()

        if phase not in {"bandit_choice", "anticipation"}:
            if "space" in valid_keys:
                key = "space"
            else:
                key = valid_keys[0]
            return Action(key=key, rt_s=rt, meta={"source": "bandit_sampler", "phase": phase, "kind": "continue"})
        p_left = self._clip_prob(factors.get("p_left", 0.5))
        p_right = self._clip_prob(factors.get("p_right", 0.5))

        if self._random() < self.exploration:
            key = self.left_key if self._random() < 0.5 else self.right_key
            if key not in valid_keys:
                key = valid_keys[0]
            return Action(
                key=key,
                rt_s=rt,
                meta={
                    "source": "bandit_sampler",
                    "policy": "explore",
                    "p_left": p_left,
                    "p_right": p_right,
                },
            )

        logits = self.inverse_temp * (p_left - p_right) + self.bias_left
        logits = max(-60.0, min(60.0, logits))
        prob_left = 1.0 / (1.0 + math.exp(-logits))
        choose_left = self._random() < prob_left
        preferred = self.left_key if choose_left else self.right_key
        if preferred not in valid_keys:
            preferred = valid_keys[0]
        return Action(
            key=preferred,
            rt_s=rt,
            meta={
                "source": "bandit_sampler",
                "policy": "softmax",
                "prob_left": prob_left,
                "p_left": p_left,
                "p_right": p_right,
            },
        )
