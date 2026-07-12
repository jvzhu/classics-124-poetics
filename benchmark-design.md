# Benchmark design: recension-aware evaluation for *Jin Ping Mei* scholarship

## Motivation

Current LLMs are trained on an undifferentiated mass of secondary discussion about *Jin Ping Mei*, its recensions, and its commentarial tradition. This flattens two textually distinct lineages (*cihua* / Recension A and *xiuxiang* / Recension B) and their correspondingly distinct commentarial apparatuses (the Chongzhen commentator and Zhang Zhupo, respectively) into a single undifferentiated "the novel." This benchmark is designed to measure whether a model can maintain the relevant distinctions rather than collapsing them.

## Task categories

### 1. Recension identification
Given a passage (in Chinese or in Roy's English translation), identify which recension it belongs to, or flag if the passage's recension is ambiguous/contested. Distractor items should include passages present in both recensions with minor variants, to test sensitivity rather than rote memorization.

### 2. Anachronism detection
Given a critical claim that applies Zhang Zhupo's commentary to a passage, determine whether that passage exists in the *xiuxiang* text Zhang actually annotated, or only in the *cihua* text (in which case applying Zhang's specific structural claim is anachronistic/unsupported). This is the core diagnostic task motivating the project.

### 3. Commentarial attribution
Given an unattributed critical claim about the novel, correctly classify its likely source lineage: Zhang Zhupo, the Chongzhen commentator, or modern Anglophone criticism (e.g., claims in the register of Naifei Ding's discourse-analytic approach). Tests whether the model can distinguish argumentative styles and concerns characteristic of each tradition, not just keyword-match names.

### 4. Frame-vs-text discrimination
Given a moral or interpretive claim about a scene, determine whether the claim is licensed by something in the text itself or is being imported from an external interpretive frame (structural theory, authorial-genius claims, decorum norms). This operationalizes the project's broader "external frame" thesis as a scored task, rather than only as an essayistic argument.

## Data sources

- Roy's five-volume Princeton translation (Recension A / *cihua*) — passages and accompanying endnotes.
- Modern critical editions of the *xiuxiang* text carrying Zhang Zhupo's commentary.
- Secondary literature (Ding and others) for the commentarial-attribution task's distractor set.

## Annotation approach

Given the specialized nature of the source material, gold-standard labels will need expert annotation (recension identity, commentarial source) rather than crowd-sourcing. This is the primary resource constraint the Kaggle Benchmark Resource Grant application is intended to address — compute and hosting for a benchmark whose ground truth requires domain expertise to construct.

## Relationship to the rest of the repository

This benchmark is the applied/evaluative counterpart to the comparative-poetics argument developed in `cross-synthesis.md` and the unit notes: the argument that interpretive frames produce rather than merely describe textual meaning is here converted into a falsifiable question about whether a model can detect *when* a frame has been mismatched to its text.

## Status

Design stage. Not yet implemented as a scored dataset. `scripts/pdf_metadata_extractor.py` supports the citation-management side of building the underlying source corpus (CSL-JSON export for Zotero), but does not yet include annotation tooling for the benchmark tasks themselves.
