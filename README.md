## Sony Aperios Open-R

A focused repo of agentic knowledge for Aibo Open-R development and debugging, extracted from the experience of persons engaging on the old Sony BBS.

## Context

- Expert summary context: [context/openr_bbs_context.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/context/openr_bbs_context.md)
- Troubleshooting rules: [context/openr_bbs_troubleshooting_rules.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/context/openr_bbs_troubleshooting_rules.md)
- Error index: [context/openr_bbs_error_index.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/context/openr_bbs_error_index.md)
- Model index: [context/openr_bbs_model_index.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/context/openr_bbs_model_index.md)
- Topic index: [context/openr_bbs_topic_index.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/context/openr_bbs_topic_index.md)


## Roadmap

- Execution roadmap: [ROADMAP.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/ROADMAP.md)
- Claim schema: [schemas/claim_record.schema.json](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/schemas/claim_record.schema.json)
- Evaluation scaffold: [eval/README.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/eval/README.md)
- Execution checklist: [tasks/execution_checklist.md](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/tasks/execution_checklist.md)

## Data

- Full message corpus JSON: [data/openr_bbs_messages.json](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/data/openr_bbs_messages.json)
- Full message corpus JSONL: [data/openr_bbs_messages.jsonl](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/data/openr_bbs_messages.jsonl)
- Full message corpus CSV: [data/openr_bbs_messages.csv](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/data/openr_bbs_messages.csv)
- Thread index: [data/openr_bbs_threads.json](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/data/openr_bbs_threads.json)
- Troubleshooting rules JSON: [data/openr_bbs_rules.json](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/data/openr_bbs_rules.json)
- Corpus manifest: [data/openr_bbs_manifest.json](/home/cartheur/ame/aiventure/aiventure-github/cartheur-aibo/open-r-dev-knowledge/data/openr_bbs_manifest.json)

Each message record includes:

- message id
- raw and normalized title
- author and timestamp
- source HTML file
- inferred reply depth, `parent_id`, and `thread_root_id`
- detected models, topics, and error signatures
- cleaned message body

## Regenerate

Run:

```bash
python3 scripts/parse_openr_bbs.py
```

This reparses the two HTML archives in `src/` and rebuilds the corpus and retrieval artifacts.

## Current Quality

Current quality rating: `9.0/10`

Why it is strong:

- the corpus is now reproducible from source HTML
- all 1,955 messages are available in machine-readable formats
- thread structure, topics, models, and error signatures are indexed
- practical troubleshooting rules are extracted into both human-readable and JSON forms
- the repo now supports retrieval, rule-based prompting, and source-backed debugging workflows

What still keeps it below `9.5-10/10`:

- topic/model/error tagging is heuristic rather than hand-curated
- there is not yet a gold-standard validation set for retrieval quality
- some important concepts are still embedded in free text instead of a stricter ontology
- reply-parent inference is structural and should be treated as high-confidence, not perfect
- no benchmark yet measures answer quality for real OPEN-R debugging questions

Best next improvements:

- add a curated evaluation set of real debugging questions and expected answers
- refine taxonomy and aliases for OPEN-R, Aperios, models, services, and config artifacts
- add higher-precision rule extraction for APIs, files, and known failure signatures
- score retrieval quality against representative expert queries
