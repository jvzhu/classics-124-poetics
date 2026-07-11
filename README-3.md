# classics-124-poetics

**A recension-aware benchmark and research repository for textual philology in *Jin Ping Mei* (金瓶梅) scholarship.**

Maintained by Vivien Jiaqian Zhu (朱嘉倩) — Ph.D. Candidate & Regent's Fellow, Japanese Literature, UC Berkeley; affiliated researcher, Stanford University / University of Cambridge.

---

## Overview

This repository connects two threads of research:

1. A comparative-poetics argument tracing defenses of transgressive representation across Western poetics (Plato, Aristotle, Longinus, Sidney, Butler) and the *Jin Ping Mei* commentarial tradition (Zhang Zhupo's 1695 commentary, the Chongzhen commentator, and Naifei Ding's *Obscene Things*).
2. A machine-checkable benchmark, built from that scholarship, for evaluating whether language models can reason about **textual recension** in classical Chinese fiction — specifically, whether a model can distinguish the *cihua* (1610, Wanli-era) and *xiuxiang* (Chongzhen-era, illustrated) recensions of *Jin Ping Mei*, and detect when an interpretive frame native to one recension has been anachronistically applied to an edition or translation based on the other.

## Why this benchmark

Textual recension conflation is a well-documented but under-detected category of error in Ming-Qing fiction scholarship. A central case: David Roy's widely used Princeton translation of *Jin Ping Mei* draws on the *cihua* recension, while Zhang Zhupo's commentary — routinely used to frame interpretive readings of the novel, including in translation apparatus — was written for the *xiuxiang* recension, a different textual base. Because the two recensions diverge in structurally meaningful ways, importing one recension's interpretive tradition onto the other risks misreading authorial intent that the *xiuxiang* commentator was never actually addressing.

This is a scoped, checkable capability: given a passage and its accompanying interpretive apparatus, can a system correctly identify the textual recension in play, and flag when commentary and text don't actually share a textual base?

## Repository structure

```
classics-124-poetics/
├── README.md                        (this file)
├── comps/                           argument-stage files connecting Western poetics
│                                     to Jin Ping Mei commentarial scholarship
├── benchmark/
│   ├── recension_schema.json        JSON Schema defining the evaluation record format
│   ├── recension_examples.json      scaffold examples (placeholders, not real excerpts)
│   └── validate_recension_dataset.py   validation + dataset statistics script
└── LICENSE
```

## The benchmark

Three task types, defined in `benchmark/recension_schema.json`:

| Task | Description |
|---|---|
| `recension_attribution` | Identify which recension (*cihua* / *xiuxiang*) a given passage is drawn from. |
| `commentary_provenance` | Match a commentary note to the recension it was originally written for. |
| `anachronism_detection` | Given a translation/edition and its accompanying interpretive framing, determine whether that framing is consistent with the recension the translation is actually based on. |

`anachronism_detection` is the hardest and most distinctive task — it operationalizes the Roy/Zhang Zhupo case as a general test of recension-aware reasoning, rather than simple text classification.

Run `python benchmark/validate_recension_dataset.py benchmark/recension_examples.json` to validate any dataset file against the schema and see split/task/difficulty balance.

## A note on source text and copyright

This repository does **not** redistribute full passages from copyrighted editions or translations — including David Roy's Princeton translation or published commentary editions of Zhang Zhupo and the Chongzhen commentator. Dataset records store bibliographic citations and short (under-15-word) excerpts or paraphrased summaries only. Building out a full evaluation set requires sourcing passages from your own licensed copies of the relevant editions.

## Status

Early stage. The comps-repo argument files establish the scholarly throughline; the benchmark schema and tooling are built; the evaluation dataset itself is being populated incrementally.

## Related work referenced

- David Roy (trans.), *The Plum in the Golden Vase* (Princeton University Press) — Princeton translation of the *cihua* recension.
- Zhang Zhupo, 1695 commentary on the *xiuxiang* recension.
- Naifei Ding, *Obscene Things: The Sexual Politics of Jin Ping Mei* (Duke University Press, 2002).
- Judith Butler's performativity framework, as a comparative lens for cross-tradition gender-performance readings.

## Contact

- ORCID: [0000-0002-1789-5272](https://orcid.org/0000-0002-1789-5272)
- Site: [vivienjiaqianzhu.com/book](https://www.vivienjiaqianzhu.com/book)
