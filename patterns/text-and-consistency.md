# Text and consistency

These target-side checks find local surface patterns. They cannot establish semantic accuracy or consistency across a whole project.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## T01 — Consecutive repeated English words

```regex
(?i)\b([a-z]+)[ \t\u00A0\u202F]+\1\b
```

**QA purpose:** Find adjacent repetitions of the same alphabetic token using a backreference.

**Language / locale assumptions:** English words written with unaccented Latin letters; case-insensitive. One or more horizontal spaces may separate the words.

**Limits / likely false positives:** “Had had” and “that that” can be grammatical. Compounds and contractions are not parsed; punctuation and line breaks interrupt matching. Not a multilingual repeated-word detector.

**Action:** Flag for human review. Read the clause before deleting a word; automatic deduplication can change meaning.

**Provenance:** Adapted from translator notes; narrowed from generic word characters and whitespace.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Check the the valve."` | `["the the"]` | Candidate accidental repetition. |
| `"The the valve is closed."` | `["The the"]` | Case-insensitive match. |
| `"Check the\u00a0the valve."` | `["the\u00a0the"]` | NBSP separator. |
| `"Check the valve."` | `[]` | Useful non-match. |
| `"She had had enough."` | `["had had"]` | Known false positive: grammatical repetition. |
| `"No, no."` | `[]` | Punctuation interrupts the repetition. |
| `"the\nthe"` | `[]` | Does not cross a line break. |
| `"123 123"` | `[]` | Numeric tokens excluded. |
| `"café café"` | `[]` | Accented words outside the stated scope. |

## T02 — Segment ending in a letter or digit

```regex
^[^\r\n]*[A-Za-z0-9][ \t\u00A0\u202F]*$
```

**QA purpose:** Find candidate missing final punctuation in a set of English prose sentences.

**Language / locale assumptions:** Select sentence-like content first. ASCII letter/digit ending, optional trailing horizontal whitespace; multiline off. Match is the whole segment.

**Limits / likely false positives:** Headings, UI labels and list items often correctly lack punctuation. Closing quotes/brackets, non-ASCII endings and already-present but incorrect punctuation are not covered. This does not compare source and target punctuation.

**Action:** Flag for review only. Classify the content and consult the style guide before adding a full stop.

**Provenance:** Illustrative implementation of the supplied final-punctuation candidate.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Close the valve"` | `["Close the valve"]` | Candidate missing full stop in a sentence. |
| `"Set pressure to 5 "` | `["Set pressure to 5 "]` | Digit ending and trailing space. |
| `"Close the valve."` | `[]` | Useful non-match. |
| `"Select “Start”."` | `[]` | Punctuated quotation. |
| `"Installation"` | `["Installation"]` | Known false positive: heading. |
| `"Select “Start”"` | `[]` | Known miss: closing quote without final punctuation. |
| `"Café"` | `[]` | Non-ASCII final letter outside scope. |
| `"Close\nthe valve"` | `[]` | Multi-line input excluded. |
| `""` | `[]` | Empty input excluded. |

