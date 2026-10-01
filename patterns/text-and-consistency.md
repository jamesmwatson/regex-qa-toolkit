# Text and consistency

These checks help me find repeated words and possible missing punctuation in translated text. Each match still needs to be read in context; neither check tells me whether the translation conveys the source correctly.

The examples below double as test fixtures. JSON strings make invisible characters visible; `[]` means the pattern should not match.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## T01 — Consecutive repeated English words

```regex
(?i)\b([a-z]+)[ \t\u00A0\u202F]+\1\b
```

**What it catches:** A word repeated immediately after itself, such as `the the`.

**When I'd use it:** After editing or post-editing English text, when a rewritten phrase may have left an accidental repeated word behind.

**Watch out for:** Repetitions such as `had had` and `that that` can be perfectly grammatical. The check is aimed at unaccented English words and ignores differences in case. Spaces and tabs can separate the words, but punctuation and line breaks interrupt the match.

**If found:** Read the clause before deleting anything. I’d remove an accidental duplicate, but keep a repetition that the grammar or meaning requires.

| Input | Expected matches | Review note |
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

**What it catches:** Segments that may be missing final punctuation, such as `Close the valve`.

**When I'd use it:** On full sentences in instructions or running prose. I’d select that material first, rather than run the check indiscriminately over headings, UI labels and lists.

**Watch out for:** Those shorter text types often need no final punctuation. This deliberately narrow check looks for an ASCII letter or digit at the end, allowing trailing horizontal whitespace. It misses unpunctuated text ending in a closing quote, bracket or non-ASCII letter, and it won’t spot an incorrect punctuation mark that is already present. Keep multiline mode off; in Python, the end anchor also permits a match just before a final newline.

**If found:** Decide whether the segment is a full sentence and check the project style. I’d add appropriate punctuation where it is missing, or leave a heading or label as it stands. The source can help clarify the context, but its punctuation may not be right for the target.

| Input | Expected matches | Review note |
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