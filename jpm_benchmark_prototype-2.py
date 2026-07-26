"""
Prototype: Jin Ping Mei recension-aware benchmark
Built against kaggle_benchmarks (Kaggle/kaggle-benchmarks).

Verified compatible with stable release v0.6.1 (tag: v0.6.1, commit e5c5222,
released 2026-06-17) -- @kbench.task, .evaluate(), assess_response_with_judge,
and kbench.judge_llm are all present unchanged between v0.6.1 and the `ci`
branch's user_guide.md as of this writing. Pin accordingly:

    pip install kaggle-benchmarks==0.6.1

Maps the three task_types already defined in recension_schema.json /
recension_examples.json onto @kbench.task functions:

  1. recension_attribution   -> classify a passage as cihua / xiuxiang
  2. commentary_provenance   -> identify which recension a commentary note
                                 was originally written for
  3. anachronism_detection   -> judge whether a passage layers Zhang Zhupo's
                                 commentary onto a Recension-A (Roy) text --
                                 the core "anachronistic importation" error
                                 from your benchmark-design.md thesis

NOTE: recension_examples.json currently contains only 3 scaffold/placeholder
records (one per task_type) with [PLACEHOLDER] text -- this script is wired
to run against real data once passage_excerpt / rationale / commentary
fields are filled in from licensed sources. Do NOT commit full copyrighted
passage text to the public repo; keep to <15-word excerpts or paraphrase,
per the schema's own instruction.
"""

import json
import pandas as pd
import kaggle_benchmarks as kbench


# ---------------------------------------------------------------------------
# 1. Load and split the dataset by task_type
# ---------------------------------------------------------------------------

def load_dataset(path: str = "recension_examples.json") -> pd.DataFrame:
    with open(path, encoding="utf-8") as f:
        records = json.load(f)
    df = pd.DataFrame(records)
    return df


def split_by_task(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {t: g.reset_index(drop=True) for t, g in df.groupby("task_type")}


# ---------------------------------------------------------------------------
# 2. Task 1 -- recension_attribution
#    Simple bool-return task: does the model's answer match gold_label?
# ---------------------------------------------------------------------------

@kbench.task(name="recension_attribution")
def recension_attribution(llm, passage_excerpt: str, gold_label: str) -> bool:
    """Given a passage, classify it as cihua or xiuxiang recension."""
    prompt = (
        f"Given the following Jin Ping Mei passage (or paraphrase): "
        f"{passage_excerpt}\n\n"
        f"Which textual recension does this passage most likely belong to "
        f"-- cihua (詞話本, 1610) or xiuxiang (繡像本, Chongzhen-era, "
        f"illustrated)? Answer with just the recension name."
    )
    response = llm.prompt(prompt)
    return gold_label.lower() in response.lower()


# ---------------------------------------------------------------------------
# 3. Task 2 -- commentary_provenance
#    Same bool-return pattern, but keyed on the commentary note rather than
#    the passage itself.
# ---------------------------------------------------------------------------

@kbench.task(name="commentary_provenance")
def commentary_provenance(llm, note_summary: str, gold_label: str) -> bool:
    """Given a commentary note, identify which recension it was written for."""
    prompt = (
        f"The following commentary note accompanies a Jin Ping Mei passage: "
        f"{note_summary}\n\n"
        f"Which recension was this commentary tradition originally written "
        f"for -- cihua or xiuxiang? Answer with just the recension name."
    )
    response = llm.prompt(prompt)
    return gold_label.lower() in response.lower()


# ---------------------------------------------------------------------------
# 4. Task 3 -- anachronism_detection
#    This is the core thesis test (Zhang Zhupo commentary anachronistically
#    layered onto Roy's Recension-A translation). It needs nuanced judgment
#    rather than a keyword match, so it uses assess_response_with_judge.
# ---------------------------------------------------------------------------

@kbench.task(name="anachronism_detection")
def anachronism_detection(llm, passage_excerpt: str, note_summary: str) -> None:
    """
    Given a passage + an attached commentary note, judge whether the model
    correctly flags an anachronistic pairing (Zhang Zhupo's commentary,
    written for xiuxiang, applied to a Recension-A/cihua-sourced passage --
    e.g. Roy's Princeton translation).
    """
    prompt = (
        f"Passage (or paraphrase): {passage_excerpt}\n\n"
        f"Attached commentary note: {note_summary}\n\n"
        f"Is there anything textually or historically inconsistent about "
        f"pairing this commentary with this passage? Explain your reasoning."
    )
    response = llm.prompt(prompt)

    assess_report = kbench.assertions.assess_response_with_judge(
        criteria=(
            "The response identifies that Zhang Zhupo's 1695 commentary "
            "was written for the xiuxiang recension.",
            "The response identifies that David Roy's Princeton translation "
            "is based on the cihua (Recension A) text.",
            "The response explicitly flags the mismatch as anachronistic "
            "or inappropriate, rather than treating the commentary as "
            "unproblematically applicable.",
        ),
        response_text=response,
        judge_llm=kbench.judge_llm,
    )
    for result in assess_report.results:
        kbench.assertions.assert_true(
            result.passed,
            expectation=f"Criterion: {result.criterion}. Reason: {result.reason}",
        )


# ---------------------------------------------------------------------------
# 5. Run all three tasks against the (currently scaffold) dataset
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = load_dataset()
    by_task = split_by_task(df)

    if "recension_attribution" in by_task:
        sub = by_task["recension_attribution"][["passage_excerpt", "gold_label"]]
        runs = recension_attribution.evaluate(llm=[kbench.llm], evaluation_data=sub)
        print("recension_attribution accuracy:", runs.as_dataframe()["result"].mean())

    if "commentary_provenance" in by_task:
        sub = by_task["commentary_provenance"].copy()
        sub["note_summary"] = sub["commentary"].apply(lambda c: c["note_summary"])
        sub = sub[["note_summary", "gold_label"]]
        runs = commentary_provenance.evaluate(llm=[kbench.llm], evaluation_data=sub)
        print("commentary_provenance accuracy:", runs.as_dataframe()["result"].mean())

    if "anachronism_detection" in by_task:
        sub = by_task["anachronism_detection"].copy()
        sub["note_summary"] = sub["commentary"].apply(lambda c: c["note_summary"])
        sub = sub[["passage_excerpt", "note_summary"]]
        anachronism_detection.evaluate(llm=[kbench.llm], evaluation_data=sub)
