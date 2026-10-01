# Test cases and validation

Run from the repository root with Python 3.10 or later:

```sh
python3 tests/run_tests.py
```

The standard-library script reads the actual regex blocks and example tables in `patterns/*.md`, then checks every documented input against its **exact list of matched spans**. It also applies every check to every target in the [worked example](../examples/sample-qa-results.md), verifying the complete list of matching check IDs. No separately maintained copy of the patterns is used.

## Reading the fixtures

Each pattern page includes positive matches, useful non-matches and acceptable matches or coverage gaps. Inputs and expected results are JSON inside Markdown code spans. `[]` means no match; `["the the"]` means that exact text should be returned. JSON quoting is fixture notation, not part of the input.

| Notation | Actual character / setting |
| --- | --- |
| `\t` | Horizontal tab |
| `\n` | Line feed |
| `\u00a0` | Non-breaking space |
| `\u202f` | Narrow non-breaking space |
| `\u2013` | En dash |
| Inline `(?i)` | Case-insensitive matching for that check |
| No inline flag | Case-sensitive; no multiline or dot-all mode |

Run against one segment at a time. Matching uses non-overlapping `finditer` results, not full-match semantics unless the pattern is anchored. N04 and T02 use `$`, which permits a match just before a final line feed in Python; do not interpret that anchor as proof that the input contains no terminal newline. Internal line breaks are excluded from their intended segment shape.

The checks use explicit ASCII digits and selected English letter ranges where stated. Word boundaries and `\w` used in guards still depend on the engine's Unicode handling; they are not language identification. Case folding, combining marks and tag representation can differ between tools.

## What was verified

The initial revised collection was run with **Python 3.12.14**. The test runner reports the current totals; all twelve checks must have positive and negative fixtures. Known acceptable matches deliberately count as successful tests: the regex should find them, and the reviewer should decline the proposed correction where appropriate.

This is a bounded example suite, not measured precision/recall on a production corpus. Trados/.NET and other CAT-tool integration have not been executed here. Repeat the relevant fixtures in the intended application before enabling a rule, especially for Unicode text, inline flags, line endings and segments containing tags.

## Coverage map

| IDs | Assertions worth checking |
| --- | --- |
| S01–S03 | Horizontal whitespace versus line breaks; non-breaking spaces; English versus French spacing; two dots versus an ellipsis or path. |
| N01–N04 | Decimal versus grouping ambiguity; token boundaries; signed values; unit case; range versus subtraction; numeric selection versus an error. |
| T01–T02 | Backreference with case variation; grammatical repetition; headings; closing-quote and non-ASCII coverage gaps. |
| L01–L03 | Both colour spellings; code exceptions; explicit spelling allowlist; noun phrase versus attributive phrase. |

The script checks detection, not a replacement algorithm. Corrections in the worked example are editorial decisions under its stated brief.
