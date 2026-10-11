# Decision-model recommendation: evidence retrieval without grade inflation

Date: 2026-10-11. Public-source proposal; no runtime experiment.
Reviewed [README](https://github.com/Ethical-Tech-CoLab/brooklyn-bridge-3d/blob/f232cf92953e59e74057633847badab92f9bd4d1/README.md).
Assessment is README-led; geometry tests were not rerun for this proposal.

## Recommendation

Rank public source passages for unresolved part/geometry questions, or flag a
claim that a source does not establish. Retain registered conflicts, source
verification state and placeholders. The documented scarcity of located
geometry is a limitation to preserve, not a gap for a model to fill.

Input: part/question, retrieved passage and source metadata. Output relevant /
related / irrelevant / insufficient evidence, optionally source-support Choice.
Exact dimensions, control hashes and provenance grades stay deterministic.

## Test

Compare unchanged search and manual review with a licensed local reranker,
Jev's [citation/reranking pattern](https://docs.typesafe.ai/cookbooks/rerank_typesafe.md),
Microsoft-Decision-1 and Sage. Group by archival source and component family.
Include linked-only documents, unposed photos, inferred locations and sources
that answer a question only qualitatively.

Measure source recall, ranking usefulness, false support, calibration and
review time/cost. Preserve evidence that the current geometry is wrong.
Model agreement cannot settle an architectural conflict or become survey truth.

## Gate

Read-only offline annotations first; no changes to controls, generated models
or shared viewer adoption. Actual geometry revisions require the existing
regression and injected-defect guards. Keep original records and human review.
Exact proprietary weights are not locally offered; no API or energy savings
are measured here.
