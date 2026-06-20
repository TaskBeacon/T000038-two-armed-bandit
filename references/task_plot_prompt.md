Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Two-Armed Bandit Task
Construct: reinforcement learning / probabilistic reward learning / reversal learning
Rows/conditions:
- Block 1: left 0.75, right 0.25.
- Block 2: left 0.25, right 0.75.
- Block 3: left 0.65, right 0.35.
- Block 4: left 0.35, right 0.65.

Timeline phases:
- Block 1: Pre-choice fixation (500 ms; no response; +) -> Bandit choice (2500 ms; press F=left / J=right; P(left)=0.75, P(right)=0.25) -> Choice confirmation (400 ms; no response; selected option highlighted) -> Outcome feedback (800 ms; no response; reward 10 or no reward 0; total) -> ITI (600 ms; no response; +)
- Block 2: Pre-choice fixation (500 ms; no response; +) -> Bandit choice (2500 ms; press F=left / J=right; P(left)=0.25, P(right)=0.75) -> Choice confirmation (400 ms; no response; selected option highlighted) -> Outcome feedback (800 ms; no response; reward 10 or no reward 0; total) -> ITI (600 ms; no response; +)
- Block 3: Pre-choice fixation (500 ms; no response; +) -> Bandit choice (2500 ms; press F=left / J=right; P(left)=0.65, P(right)=0.35) -> Choice confirmation (400 ms; no response; selected option highlighted) -> Outcome feedback (800 ms; no response; reward 10 or no reward 0; total) -> ITI (600 ms; no response; +)
- Block 4: Pre-choice fixation (500 ms; no response; +) -> Bandit choice (2500 ms; press F=left / J=right; P(left)=0.35, P(right)=0.65) -> Choice confirmation (400 ms; no response; selected option highlighted) -> Outcome feedback (800 ms; no response; reward 10 or no reward 0; total) -> ITI (600 ms; no response; +)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per block probability context.
- Each row contains 5 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows participant-visible screen content only.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place block labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 18-20% of the image.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Preserve these exact terms where used: Block 1, Block 2, Block 3, Block 4, F=left, J=right, P(left), P(right), 500 ms, 2500 ms, 400 ms, 800 ms, 600 ms.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
