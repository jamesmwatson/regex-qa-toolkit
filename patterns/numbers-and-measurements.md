# Numbers and measurements

These checks can find numbers of a specific 'shape' or pattern but they can't tell what the numbers actually mean. It's important to choose the right target language conventions and project style before correcting a match.

The examples below double as test fixtures. `[]` means the pattern should not match.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## N01 — Comma inside a number

```regex
(?<![\w.,])[-+]?[0-9]+,[0-9]+(?!\w|[.,][0-9])
```

**What it catches:** Numbers containing a comma, such as `12,5`.

**When I'd use it:** In a DE→EN project, for example, to pull together numbers that may still be using a German decimal comma in the English target.

**Watch out for:** A match is not automatically wrong. `1,234` may be a perfectly valid English thousands grouping, and this check deliberately ignores more complicated forms such as `1.234,56`. It also won't match `12,5mm` while the unit is attached; N02 can catch that first.

**If found:** Compare it with the source before changing anything. A blind comma-to-point replacement could turn `1,234` into a completely different number.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"Thickness: 12,5 mm."` | `["12,5"]` | Candidate German decimal in an English target. |
| `"Offset: -0,5 mm."` | `["-0,5"]` | Signed decimal. |
| `"3,14159 versus 3.14159."` | `["3,14159"]` | Retained original fixture. |
| `"Thickness: 12.5 mm."` | `[]` | Useful non-match: decimal point. |
| `"Batch: 1,234."` | `["1,234"]` | Known ambiguity: English thousands grouping may be correct. |
| `"Value: 1.234,56 EUR."` | `[]` | Excluded mixed separators, not a clean bill of health. |
| `"Value: 1,234,567."` | `[]` | Excluded multiple separators. |
| `"Thickness: 12,5mm."` | `[]` | Known miss: unit attached to number; review with N02 and rerun. |
| `"ID A12,5B"` | `[]` | Do not match inside an identifier. |

## N02 — Missing space before a selected unit

```regex
(?<![\w.,])[-+]?[0-9]+(?:[.,][0-9]+)?(?:mm|cm|kg|kPa|bar|°C)(?!\w)
```

**What it catches:** Measurements where the value and unit have run together, such as `25mm` or `1,2bar`.

**When I'd use it:** On technical material where the project style requires a space between a number and units such as `mm`, `kg` or `bar`.

**Watch out for:** The unit list is deliberately small, and product names or identifiers can look like measurements. This isn't intended to be a general-purpose unit parser.

**If found:** Check that it really is a measurement, then insert the kind of space required by the project. That may be an ordinary space or a non-breaking one. Keep the value and unit case unchanged.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"Length: 25mm."` | `["25mm"]` | Candidate missing space. |
| `"Temperature: -5°C."` | `["-5°C"]` | Degree-Celsius symbol. |
| `"Pressure: 1,2bar."` | `["1,2bar"]` | Comma decimal recognised, not approved. |
| `"Length: 25 mm."` | `[]` | Useful non-match. |
| `"Length: 25\u00a0mm."` | `[]` | Existing NBSP is acceptable to this check. |
| `"Length: 25MM."` | `[]` | Wrong unit case needs a separate check. |
| `"Type A25mm"` | `[]` | Attached identifier excluded. |
| `"Part 25mm-series"` | `["25mm"]` | Known false positive: product naming. |
| `"Length: 25m."` | `[]` | Unlisted unit: known coverage gap. |

## N03 — Hyphenated measurement range

```regex
(?<![\w.,+\-−])[0-9]+(?:[.,][0-9]+)?[ \t\u00A0\u202F]*-[ \t\u00A0\u202F]*[0-9]+(?:[.,][0-9]+)?[ \t\u00A0\u202F]*(?:mm|cm|kg|kPa|bar|°C)(?!\w)
```

**What it catches:** Measurement ranges written with an ASCII hyphen, such as `15-20 mm`.

**When I'd use it:** When the project style calls for an en dash or the word `to` in numerical ranges.

**Watch out for:** Regex can't tell whether `15-20` is really a range rather than subtraction or part of a product code. Signed ranges are outside this check.

**If found:** Check the source and surrounding text, then change the separator if the project style requires it. In the fictional project used here, `15-20 mm` becomes `15–20 mm`.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"Length: 15-20 mm."` | `["15-20 mm"]` | Candidate hyphenated range. |
| `"Pressure: 0.8 - 1.2 bar."` | `["0.8 - 1.2 bar"]` | Spaced hyphen and decimal points. |
| `"Length: 15-20\u202fmm."` | `["15-20\u202fmm"]` | Preserve the unit space choice. |
| `"Length: 15–20 mm."` | `[]` | Useful non-match: en dash. |
| `"Length: 15 to 20 mm."` | `[]` | Written range. |
| `"Temperature: -5-10 °C."` | `[]` | Signed range excluded. |
| `"Code A15-20 mm"` | `[]` | Identifier prefix excluded. |
| `"Calculation: 15-20 mm."` | `["15-20 mm"]` | Known false positive: subtraction in context. |

## N04 — All-numeric segment filter

```regex
^[ \t\u00A0\u202F]*[+-]?[0-9]+(?:[.,][0-9]+)?[ \t\u00A0\u202F]*$
```

**What it catches:** Segments made up almost entirely of a single number.

**When I'd use it:** As a quick filter for reviewing source and target values together. Numeric-only segments are easy to overlook because there is very little linguistic context around them.

**Watch out for:** A match says nothing about whether the value or separator is correct. Dates, percentages, scientific notation and more complex grouped numbers are outside this deliberately narrow pattern.

**If found:** Compare source and target and leave it alone if the value and formatting are appropriate. This rule is for finding material to inspect, not fixing it automatically.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"123"` | `["123"]` | Select an integer. |
| `" -12,5 "` | `[" -12,5 "]` | Select a signed value with surrounding spaces. |
| `"1,234"` | `["1,234"]` | Ambiguous grouping; still only a filter. |
| `"123\n"` | `["123"]` | The end anchor permits a terminal LF; see test conventions. |
| `"12 mm"` | `[]` | Useful non-match: contains a unit. |
| `"Part 123"` | `[]` | Not numeric-only. |
| `"1,234,567"` | `[]` | Multiple separators excluded. |
| `""` | `[]` | Empty segment excluded. |
| `"١٢٣"` | `[]` | Non-ASCII digits outside scope. |

