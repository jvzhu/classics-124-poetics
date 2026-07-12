# classics-124-poetics

Comparative poetics research repository connecting Western literary theory (via UC Berkeley Classics 124, G.R.F. Ferrari, Spring 2016) to the Ming-Qing Chinese commentarial tradition, centered on *Jin Ping Mei* (金瓶梅) and Zhang Zhupo's 1695 commentary.

Course reference: <https://dagrs.berkeley.edu/courses/spring-2016>

## Core argument

Defenses of transgressive representation — in Western poetics (Plato's expulsion of the poets, Aristotle's catharsis, Longinus's sublime, Sidney's *Apology*) and in the *Jin Ping Mei* commentarial tradition alike — consistently locate their justification in an external interpretive frame. That frame does not merely describe the moral and gender categories it invokes; it *produces* them. This repository traces that pattern across two traditions that rarely get read together, and treats Judith Butler's account of performativity as a shared analytic lens for both.

## Repository contents

- **`unit-notes/`** — reading notes on the core Western poetics figures (Plato, Aristotle, Longinus, Sidney, and the neoclassical reception).
- **`western-poetics-synthesis.md`** — cross-cutting synthesis of the Western unit, isolating the "external frame" move each figure makes.
- **`jin-ping-mei/`** — three comparative files on the Chinese-language side: Zhang Zhupo's commentary against the Chongzhen commentator, Naifei Ding's *Obscene Things* as the dominant English-language reading, and the textual crux in David Roy's Princeton translation.
- **`butler-gender-trouble-foundation.md`** — theoretical foundation file on performativity, used as the connective tissue between both traditions.
- **`adjacent-scholarship/`** — related work extending the project's "external frame" thesis beyond its two main traditions (currently: Xiaofei Tian on letters and gift-giving in early medieval China).
- **`cross-synthesis.md`** — the full comparative argument, Western poetics ↔ Ming-Qing commentary ↔ performativity.
- **`benchmark-design.md`** — design notes for a recension-aware LLM benchmark (see below).
- **`scripts/pdf_metadata_extractor.py`** — utility for extracting citation metadata from PDF sources into CSL-JSON for Zotero import.

## The recension problem

*Jin Ping Mei* survives in two major textual traditions:

- **Recension A (詞話本 / *cihua*, 1610)** — the version underlying David Roy's five-volume Princeton translation.
- **Recension B (繡像本 / *xiuxiang*, illustrated edition)** — the version Zhang Zhupo actually annotated in 1695.

Because Roy's translation is keyed to Recension A while Zhang Zhupo's commentary was written against Recension B, any reading that layers Zhang's interpretive apparatus directly onto Roy's English text is importing a commentarial frame onto a textual base it was never written for. This is a real and easy-to-miss error — one that current LLMs, trained on a flattened, undifferentiated mass of secondary discussion, are especially prone to reproduce uncritically.

## Benchmark motivation

This repository underpins a proposed recension-aware benchmark (see `benchmark-design.md`) measuring whether an LLM can:

1. Correctly distinguish *cihua* vs. *xiuxiang* recensions when given a passage or a citation.
2. Detect anachronistic importation of Zhang Zhupo's commentary onto material sourced from Roy's Recension-A translation.
3. Correctly attribute claims to the right critical lineage (Zhang Zhupo vs. the Chongzhen commentator vs. modern Anglophone criticism such as Naifei Ding's *Obscene Things*).

## Status

Active research repository, maintained by Vivien Jiaqian Zhu (朱嘉倩), Ph.D. candidate, Department of East Asian Languages and Cultures, UC Berkeley. Visiting scholar, Stanford University; Fellow, University of Cambridge.

ORCID: [0000-0002-1789-5272](https://orcid.org/0000-0002-1789-5272)
