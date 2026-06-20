# Task Plot Brief

## Task

- Title: Two-Armed Bandit Task
- Construct: reinforcement learning / probabilistic reward learning / reversal learning
- Paradigm: choose left or right bandit under block-wise reward probability reversals.

## Rows

- Block 1: left 0.75, right 0.25.
- Block 2: left 0.25, right 0.75.
- Block 3: left 0.65, right 0.35.
- Block 4: left 0.35, right 0.65.

## Trial Timeline

1. Pre-choice fixation: 500 ms. Show central fixation, no response.
2. Bandit choice: 2500 ms. Show left/right options. Press F for left, J for right.
3. Choice confirmation: 400 ms. Highlight selected option.
4. Outcome feedback: 800 ms. Show reward or no reward and running total.
5. ITI: 600 ms. Show fixation before next trial, no response.

## Notes

- Reward is 10 for win and 0 for no reward.
- No-response policy can impute a random choice.
- Reward probabilities are stable within a block and change across blocks.
