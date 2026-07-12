# David Roy's Princeton translation and the recension crux

## The crux, stated precisely

David Tod Roy's five-volume *The Plum in the Golden Vase* (Princeton UP, 1993–2013) is a complete, heavily annotated English translation of *Jin Ping Mei*. Roy's base text is **Recension A — the *cihua* (詞話本) edition of 1610**, the earliest complete surviving printed text, distinguished by its extensive use of *ci* song-lyrics and a somewhat looser, more colloquial narrative texture.

**Zhang Zhupo's 1695 commentary, by contrast, was written against Recension B — the *xiuxiang* (繡像本, "illustrated") edition**, a later, more polished redaction that trims much of the *cihua* text's song-lyric material and tightens the prose.

These are not trivially different printings of "the same novel" — they represent two distinct editorial/textual lineages with real differences in content, emphasis, and structure. Zhang Zhupo's structural readings (the parallelism, the "cold/hot" patterning, the *dufa* essays) are built from close attention to the *xiuxiang* text's specific wording and organization.

## The error this project is built to catch

When a reader — human or machine — takes Roy's Recension-A English translation and reads it *through* Zhang Zhupo's commentary (whether via secondary literature quoting Zhang, or via a scholar layering Zhang's structural claims onto Roy's text), they are importing an interpretive frame onto a textual base it was not built for. Some of Zhang's specific structural observations may not hold, in the same form, against the *cihua* text Roy actually translated. This is a textual-historical error masquerading as a routine critical move, because most Anglophone secondary literature does not consistently flag which recension is under discussion.

## Why this is an LLM benchmark problem

Large language models trained on the undifferentiated mass of secondary discussion about "*Jin Ping Mei* and its commentary" have no inherent mechanism for tracking which recension a given claim is actually keyed to. A model asked to explain Zhang Zhupo's reading of a scene, if given only Roy's English text as the passage in question, has no principled way to know whether that specific scene exists in the same form (or exists at all) in the *xiuxiang* text Zhang was actually commentating on — unless it has been specifically trained or prompted to check. This project's benchmark design (`benchmark-design.md`) is built to test exactly this failure mode.

## Working bibliography note

- Roy, David Tod, trans. *The Plum in the Golden Vase, or, Chin P'ing Mei*. 5 vols. Princeton University Press, 1993–2013. [Recension A / *cihua*]
- Zhang Zhupo commentary editions are most accessible via modern critical reprints of the *xiuxiang*-descended text; any citation of Zhang's commentary in this project should specify the edition used, since commentary transmission itself has its own textual history.
