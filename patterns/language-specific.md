# English and locale-specific checks

These English examples make their lexical and house-style assumptions explicit. They are not universal UK/US conversion rules or a multilingual language detector.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## L01 — Color / colour inventory

```regex
(?i)\bcolou?r\b
```

**QA purpose:** Find both spellings so a reviewer can assess project consistency.

**Language / locale assumptions:** English only. The project chooses US spelling, UK spelling or explicit exceptions. This is an inventory query, not a rule declaring either spelling wrong.

**Limits / likely false positives:** CSS properties, code, quoted UI labels and product names can legitimately retain “color” in UK English material. Inflected and compound forms are outside this exact-word query.

**Action:** Flag for review. Compare occurrences with the approved term and content type; preserve code and official names.

**Provenance:** Adapted from the color/colour example in translator notes; documented as an inventory check.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Choose a color."` | `["color"]` | US form found. |
| `"Choose a colour."` | `["colour"]` | UK form found too; not an error by itself. |
| `"COLOR / colour"` | `["COLOR", "colour"]` | Case-insensitive inventory. |
| `"Choose a shade."` | `[]` | Useful non-match. |
| `"discoloration"` | `[]` | No substring match. |
| `"colors"` | `[]` | Plural intentionally outside scope. |
| `"CSS color: red;"` | `["color"]` | Known acceptable match: code token. |

## L02 — Selected -ize forms under an -ise house style

```regex
(?i)\b(?:organi|locali|optimi|customi)z(?:e|es|ed|ing|ation|ations)\b
```

**QA purpose:** Find selected z-spellings when a project explicitly requires the corresponding s-spellings.

**Language / locale assumptions:** English; a small allowlist of organise, localise, optimise and customise word families. UK English does not universally require -ise: some UK styles accept or prefer -ize.

**Limits / likely false positives:** This is a lexical allowlist, not morphological analysis or a dictionary. Other word families and protected names are not resolved. Case-insensitive matches do not provide a case-preserving replacement.

**Action:** Flag for review. Consult the house style and change approved words individually; do not replace every “iz” or “z” globally.

**Provenance:** Adapted from a generated earlier suggestion; broad suffix replacement rejected in favour of an explicit, tested allowlist.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Optimize the process."` | `["Optimize"]` | Selected word family. |
| `"Review localization and customized labels."` | `["localization", "customized"]` | Noun and inflected verb. |
| `"Optimise the process."` | `[]` | Useful non-match: s-spelling. |
| `"Check size and prize."` | `[]` | Exception words never enter the allowlist. |
| `"Do not capsize or seize it."` | `[]` | More counterexamples to blanket replacement. |
| `"Analyze the result."` | `[]` | Unlisted spelling difference outside scope. |
| `"Product name: Optimize."` | `["Optimize"]` | Known acceptable match if it is a protected name. |

## L03 — Unhyphenated state of the art

```regex
(?i)\bstate[ \t\u00A0\u202F]+of[ \t\u00A0\u202F]+the[ \t\u00A0\u202F]+art\b
```

**QA purpose:** Find the unhyphenated phrase for a grammatical and house-style review.

**Language / locale assumptions:** English; horizontal whitespace only. The query intentionally finds noun-phrase and attributive uses alike.

**Limits / likely false positives:** “The state of the art is changing” is correct. A following word does not prove the phrase is an adjective before a noun; regex does not parse its grammatical role.

**Action:** Flag for human review. Hyphenate “state-of-the-art equipment” if the style requires it; retain the noun phrase in “the state of the art”.

**Provenance:** Adapted from a generated earlier suggestion; removed the misleading next-word test and automatic replacement.

Examples are executable fixtures: JSON strings expose invisible characters; `[]` means no match.

| Input | Expected matched spans | Review note |
| --- | --- | --- |
| `"Use state of the art equipment."` | `["state of the art"]` | Candidate attributive phrase. |
| `"STATE OF THE ART equipment"` | `["STATE OF THE ART"]` | Case-insensitive. |
| `"Use state-of-the-art equipment."` | `[]` | Useful non-match: already hyphenated. |
| `"The state of the art is changing."` | `["state of the art"]` | Known acceptable noun phrase. |
| `"state of the artist"` | `[]` | Whole-word boundary. |
| `"state\nof the art"` | `[]` | No cross-line match. |

