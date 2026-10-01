# Numbers and measurements

Numeric shape is not numeric meaning. Confirm the value against the source; select the target locale and project style before correcting a match.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## N01 — Comma inside a number

```regex
(?<![\w.,])[-+]?[0-9]+,[0-9]+(?!\w|[.,][0-9])
```

**QA purpose:** Find comma-number tokens for review when the target locale expects decimal points.

**Language / locale assumptions:** ASCII digits, optional ASCII sign, one comma and no other separator. Suitable for a scoped DE→EN decimal-format review, not for identifying all numeric formats.

**Limits / likely false positives:** “1,234” may be a valid English thousands grouping or a decimal in another locale. This deliberately excludes mixed/grouped forms such as “1.234,56”; it cannot infer numeric value or compare it with the source. A number attached to a unit, such as “12,5mm”, is excluded by the token guard too; N02 can catch the missing space, then N01 can find the comma on a second pass.

**Action:** Flag only. Confirm value and grouping against the source before changing any separator. A blanket comma-to-point replacement can change a value by a factor of 1,000.

**Provenance:** Adapted from the original number checks and translator measurement notes; added token boundaries and conservative scope.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
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

**QA purpose:** Find a number attached directly to a selected unit symbol, such as “25mm”.

**Language / locale assumptions:** A project style requiring a space between the value and these exact symbols. Both decimal separators are recognised without endorsing either. Unit case is significant: do not turn on ignore-case.

**Limits / likely false positives:** The small unit list is deliberate; it is not a unit parser. Product identifiers can resemble measurements. Compound units, powers and unlisted units are not fully checked; an unlisted form may be missed or only partly matched.

**Action:** Flag for review. Confirm it is a measurement, then use the space required by the project, which may be non-breaking. Preserve unit case and value.

**Provenance:** Adapted from translator notes on number + abbreviated-unit formatting; rewritten as a narrow missing-space check.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
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

**QA purpose:** Find positive measurement ranges using an ASCII hyphen when the project calls for an en dash or “to”.

**Language / locale assumptions:** Unsigned ASCII numbers; one optional decimal part per endpoint; selected case-sensitive unit symbols. Either decimal separator is accepted for detection.

**Limits / likely false positives:** Cannot distinguish a range from subtraction or a product code. Signed ranges are intentionally excluded. Does not check ascending order or validate mixed decimal styles.

**Action:** Flag for review. For the fictional house style, “15-20 mm” becomes “15–20 mm”; other projects may require “15 to 20 mm”. There is no universal dash or spacing rule.

**Provenance:** Adapted from a generated workflow suggestion in the earlier notes; narrowed and independently tested here. Not evidence of deployment.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
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

**QA purpose:** Select simple numeric-only segments for a focused source–target review. This is a triage filter, not an error detector.

**Language / locale assumptions:** ASCII digits, optional sign and at most one comma or point; surrounding horizontal whitespace permitted. Run per segment with multiline off.

**Limits / likely false positives:** Cannot distinguish decimal separators from grouping. Does not cover scientific notation, dates, percentages or grouped numbers with multiple separators. A numeric-only target can be entirely correct.

**Action:** Filter for review; compare value and formatting with source and locale. Never change or discard a segment merely because it matches.

**Provenance:** Illustrative implementation of the supplied all-numeric-segment candidate.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
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

