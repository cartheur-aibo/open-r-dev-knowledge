# OPEN-R Dev Knowledge Roadmap

This roadmap turns `open-r-dev-knowledge` from a strong retrieval-oriented
archive into an evidence-ranked operational knowledge base for OPEN-R /
Aperios debugging.

## Goal

Produce a repo that can answer real OPEN-R debugging questions with:

- claim-level evidence, not only thread-level retrieval
- explicit model and version scope
- authority-aware ranking of sources
- contradiction tracking
- structured procedures and troubleshooting playbooks
- measurable retrieval and answer quality

## Desired End State

A future user should be able to ask a question such as:

- Why does an SDK stick appear dead on boot?
- Do we know enough to build a reliable ERS-7 8 MB stick?
- What causes `selector out of range`?
- Is this advice valid for ERS-7M3 or only ERS-210?

and receive an answer that includes:

- a compact conclusion
- confidence level
- model and version scope
- supporting messages and source authority
- conflicting evidence if present
- a recommended next-check sequence

## Current State

The repo is already strong at:

- reproducible parsing of the Sony BBS HTML archive
- message-level indexing by model, topic, and error signature
- human-readable summary context
- compact troubleshooting rules

The main remaining gap is structure.

Most high-value knowledge still lives in:

- free-text summaries
- heuristic tags
- thread/message retrieval
- non-normalized operational advice

## Principles

1. Prefer source-backed claims over summary-only guidance.
2. Preserve uncertainty instead of flattening it away.
3. Encode scope aggressively: model, firmware, SDK version, base image, and
   runtime path all matter.
4. Treat procedures and failure playbooks as first-class artifacts.
5. Make evaluation part of the repo, not an afterthought.

## Phase 1: Claim Layer

### Objective

Introduce a claim-level data model so important facts and heuristics can be
represented independently of the raw message archive.

### Deliverables

- a claim schema
- a curated seed claim set from the highest-value OPEN-R topics
- provenance links from each claim back to specific messages
- explicit fields for confidence, authority, and scope

### Initial target topics

- SDK stick boot failure
- `WCONSOLE` versus `WLAN` versus `BASIC`
- flash ROM / firmware gating
- `selector out of range`
- `... NOT FOUND`
- `sTIMEOUT` / `error 28`
- `WLANCONF.TXT` formatting
- pink-stick / programmable-stick handling and formatting risk

### Acceptance criteria

- at least 50 curated claims exist
- each claim cites one or more message ids
- each claim has a source authority rank
- each claim declares whether it is a fact, heuristic, or inference

## Phase 2: Scope And Authority

### Objective

Make claims safe to use by encoding where they apply and why they should be
trusted.

### Deliverables

- normalized scope vocabulary for model, firmware, SDK, base image, and media
- authority ranking rules
- corroboration counts and contradiction links
- explicit "unknown" and "not established" claim types

### Acceptance criteria

- high-value claims are scoped to specific models where possible
- contradicting claims can be represented without deleting either one
- admin/support posts can be ranked separately from community replies

## Phase 3: Procedures And Playbooks

### Objective

Extract operational workflows from the archive into reusable procedures.

### Deliverables

- structured procedure records
- canonical failure playbooks
- discriminators that help distinguish similar failure modes

### High-priority playbooks

- SDK stick fails to boot
- AIBO powers off after pause
- `WCONSOLE` appears dead
- WLAN works in ad-hoc but not AP mode
- service or subject `NOT FOUND`
- `selector out of range`
- queue overflow / send-ready issues

### Acceptance criteria

- each playbook has symptom, likely causes, checks, and stop conditions
- procedures list prerequisites and model/version caveats
- procedures link to claims rather than duplicating unsupported advice

## Phase 4: Evaluation

### Objective

Measure whether the repo can answer real debugging questions better over time.

### Deliverables

- an evaluation question set
- reference answer outlines
- retrieval checks
- scoring guidance for factuality, scope, and usefulness

### Seed benchmark categories

- boot/setup
- runtime wiring and selectors
- networking and WLAN
- motion and joint semantics
- stick/media handling
- model/version compatibility

### Acceptance criteria

- at least 25 benchmark questions
- each question has expected evidence anchors
- evaluation can distinguish unsupported confidence from grounded answers

## Phase 5: Regeneration And Tooling

### Objective

Make the enriched knowledge artifacts reproducible, not hand-maintained drift.

### Deliverables

- parser extensions or post-processing scripts for claim/procedure generation
- validation checks for schema conformance
- a documented workflow for curated updates

### Acceptance criteria

- a contributor can regenerate machine-readable artifacts from source plus
  curated data
- validation catches malformed records and missing provenance

## Immediate Execution Plan

### Sprint 1

- finalize claim schema
- create `claims_seed.jsonl` with the first 15-20 high-value claims
- define authority ranks and claim types
- seed the first 8-10 benchmark questions

### Sprint 2

- extract the first boot-failure playbooks
- add contradiction and corroboration fields
- link summary context statements back to claims

### Sprint 3

- extend parsing or post-processing to support artifact generation
- add validation tooling
- score the benchmark set against current retrieval outputs

## Concrete File Additions Planned

- `schemas/claim_record.schema.json`
- `eval/README.md`
- `eval/questions_seed.md`
- `tasks/execution_checklist.md`

## Risks

- over-automation may turn nuanced guidance into brittle pseudo-facts
- poor scope handling may make the system sound more certain than it is
- evaluation without real repo debugging questions may optimize for the wrong
  tasks

## Non-Goals

- reconstructing undocumented Sony internals without evidence
- pretending community guesses are equivalent to SDK support answers
- replacing the raw archive with only a curated layer

## Success Metric

This repo is meaningfully improved when it can answer a real question from
active AIBO work with less hand-holding, clearer evidence, and fewer hidden
assumptions than the current summary-only layer.
