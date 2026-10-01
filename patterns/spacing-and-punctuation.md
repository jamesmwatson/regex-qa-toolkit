# Spacing and punctuation

I’d use these checks to pick up small spacing and punctuation problems in English prose. Code, tables and other languages need a different approach: what looks like an extra space may be intentional.

## S01 — Repeated horizontal whitespace

```regex
[ \t\u00A0\u202F]{2,}
```

**What it catches:** Extra spaces or combinations of spaces and tabs, such as the double space in `Press  start.`

**When I'd use it:** During a final pass over translated prose where I’d expect single spaces between words.

**Watch out for:** Tables, code and aligned text may use repeated spaces deliberately. The check includes ordinary spaces, tabs, non-breaking spaces and narrow non-breaking spaces, but leaves line breaks alone.

**If found:** Check whether the spacing serves a purpose. In ordinary prose, I’d usually reduce an accidental run to one space, keeping a non-breaking space where the text or project style needs it.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"Press  start."` | `["  "]` | Candidate: accidental double space. |
| `"This  sentence  has  double  spaces."` | `["  ", "  ", "  ", "  "]` |  find every run. |
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

**What it catches:** Spaces before punctuation, such as `Check , then continue.` or `Ready ?`

**When I'd use it:** When reviewing English target text where the project style calls for punctuation to follow the preceding word directly.

**Watch out for:** Spacing before some punctuation is normal in French, so this is an English-target check. Mathematical notation, a number such as `0 .5`, or a spaced ellipsis needs a closer look. The match includes the punctuation as well as the preceding whitespace; line breaks are excluded.

**If found:** Read the surrounding text and remove an accidental space, keeping the punctuation. If the match belongs to another language or to notation, I’d check the relevant convention before changing it.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"Space before punctuation !"` | `[" !"]` |  |
| `"Check , then continue."` | `[" ,"]` | Candidate: space before comma. |
| `"Ready\u202f?"` | `["\u202f?"]` | Narrow NBSP in English target. |
| `"Ready?"` | `[]` | Useful non-match. |
| `"Ready\n?"` | `[]` | No cross-line match. |
| `"Prêt\u202f?"` | `["\u202f?"]` | Expected match, but acceptable under a French house style; do not enable this English rule there. |

## S03 — Exactly two consecutive full stops

```regex
(?<!\.)\.\.(?!\.)
```

**What it catches:** Two consecutive dots, such as `Done..`, which may be a doubled full stop or an incomplete ellipsis.

**When I'd use it:** In a punctuation pass over translated prose or UI strings, where an extra or missing dot is easy to overlook.

**Watch out for:** Paths such as `../manual`, code and some range notation legitimately contain `..`. The check finds exactly two ordinary full stops; it leaves `...` and `…` alone.

**If found:** Check the sentence and, where useful, the source to decide whether a full stop or an ellipsis was intended. I’d leave valid notation alone and query ambiguous wording rather than choose a replacement automatically.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"There are two dots.. right here."` | `[".."]` |  |
| `"Done.."` | `[".."]` | Detect at end of segment. |
| `"..Start"` | `[".."]` | Detect at start without consuming adjacent letters. |
| `"Wait..."` | `[]` | Useful non-match: three-dot ellipsis. |
| `"Wait…"` | `[]` | Unicode ellipsis. |
| `"Done."` | `[]` | Single full stop. |
| `"../manual"` | `[".."]` | Known false positive: relative path. |