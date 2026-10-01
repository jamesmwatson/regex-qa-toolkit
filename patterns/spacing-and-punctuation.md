# Spacing and punctuation

Enable these for the relevant English prose, not indiscriminately across code, tables or other locales.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## S01 — Repeated horizontal whitespace

```regex
[ \t\u00A0\u202F]{2,}
```

**QA purpose:** Find runs of two or more horizontal whitespace characters in prose.

**Language / locale assumptions:** Use where the project expects single inter-word spaces. Explicitly includes space, tab, NBSP (U+00A0) and narrow NBSP (U+202F); excludes line breaks.

**Limits / likely false positives:** Alignment, code and intentionally spaced tables can match. A match does not tell you which space character should survive.

**Action:** Review first. Replacing a reviewed run with one ordinary space is reasonably safe only in plain prose whose style requires ordinary spaces. Do not normalise non-breaking spaces globally.

**Provenance:** Adapted from the original repository and translator notes; horizontal scope narrowed for this edition.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Press  start."` | `["  "]` | Candidate: accidental double space. |
| `"This  sentence  has  double  spaces."` | `["  ", "  ", "  ", "  "]` | Retained original fixture; find every run. |
| `"Press \tstart."` | `[" \t"]` | Mixed horizontal whitespace. |
| `"Press\u00a0\u202fstart."` | `["\u00a0\u202f"]` | Two different non-breaking spaces. |
| `"Press start."` | `[]` | Useful non-match: one space. |
| `"Press\u00a0start."` | `[]` | Preserve a single NBSP. |
| `"Press\nstart."` | `[]` | Do not consume a line break. |
| `"A  B"` | `["  "]` | Known false positive: deliberate table alignment. |

## S02 — Whitespace before English punctuation

```regex
[ \t\u00A0\u202F]+[.,;:!?]
```

**QA purpose:** Find whitespace immediately before selected punctuation marks.

**Language / locale assumptions:** English prose under a style with no spaces before these marks. The matched span includes the punctuation.

**Limits / likely false positives:** French spacing before some punctuation is a counterexample to applying this rule across locales. A decimal written as “0 .5”, mathematical notation or a leading ellipsis needs contextual review.

**Action:** Flag for review; remove the whitespace only after confirming the punctuation and locale. Never apply as a multilingual cleanup.

**Provenance:** Adapted from the original repository and translator notes; excludes line breaks.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Space before punctuation !"` | `[" !"]` | Retained original fixture. |
| `"Check , then continue."` | `[" ,"]` | Candidate: space before comma. |
| `"Ready\u202f?"` | `["\u202f?"]` | Narrow NBSP in English target. |
| `"Ready?"` | `[]` | Useful non-match. |
| `"Ready\n?"` | `[]` | No cross-line match. |
| `"Prêt\u202f?"` | `["\u202f?"]` | Expected match, but acceptable under a French house style; do not enable this English rule there. |

## S03 — Exactly two consecutive full stops

```regex
(?<!\.)\.\.(?!\.)
```

**QA purpose:** Find two dots that may be an accidental doubled full stop or a malformed ellipsis.

**Language / locale assumptions:** Plain prose using the ASCII full stop. A three-dot ellipsis and the single ellipsis character are outside this check.

**Limits / likely false positives:** Paths, code and deliberately written ranges can contain two dots. The check cannot decide whether one dot or an ellipsis was intended.

**Action:** Flag for human review; no automatic replacement.

**Provenance:** Adapted from the original punctuation check; repaired boundaries and end-of-segment handling.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"There are two dots.. right here."` | `[".."]` | Retained original fixture. |
| `"Done.."` | `[".."]` | Detect at end of segment. |
| `"..Start"` | `[".."]` | Detect at start without consuming adjacent letters. |
| `"Wait..."` | `[]` | Useful non-match: three-dot ellipsis. |
| `"Wait…"` | `[]` | Unicode ellipsis. |
| `"Done."` | `[]` | Single full stop. |
| `"../manual"` | `[".."]` | Known false positive: relative path. |

