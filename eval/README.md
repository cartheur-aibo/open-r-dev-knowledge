# Evaluation Scaffold

This directory is for measuring whether `open-r-dev-knowledge` actually helps
answer real OPEN-R / Aperios debugging questions.

## Purpose

The current repo is rich in source material and summaries, but it does not yet
measure answer quality on realistic tasks.

The evaluation set should focus on real questions such as:

- Why does an SDK Memory Stick appear dead on boot?
- When is `WCONSOLE` the wrong base image for bring-up?
- What does `selector out of range` usually mean?
- Does 8 MB versus 16 MB matter for programmable sticks?
- What should be checked before blaming an OPEN-R sample binary?

## Suggested Files

- `questions_seed.md` for a human-curated benchmark question list
- `expected_answers/` for compact answer outlines and evidence anchors
- `retrieval_checks/` for expected source hits

## Minimum Record For Each Question

Each benchmark question should include:

- question text
- task category
- expected conclusion
- required evidence anchors such as message ids or context files
- unacceptable overclaims
- scope caveats

## Scoring Dimensions

Use at least these dimensions:

- factual grounding
- evidence quality
- scope correctness
- uncertainty handling
- operational usefulness

## Good Benchmark Design Rules

- prefer questions drawn from active repo work, not abstract trivia
- include cases where the correct answer is "not established"
- include cases with contradictory community guidance
- include model-specific questions that punish overgeneralization
