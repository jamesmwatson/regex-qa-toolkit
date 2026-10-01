# Worked example: a fictional technical review

[Overview](../README.md) · [How to run a review](trados-workflow.md)

**Brief:** review a fictional German-to-UK-English pump quick-start guide and its associated UI strings. The house style specifies decimal points, spaces before unit symbols, en dashes for positive ranges and selected `-ise` spellings. Full instructions take final punctuation; headings and UI labels do not. Official identifiers remain unchanged.

All strings below are invented. Each row is one target segment. The table lists **every check that matches**, including filters and acceptable matches. All twelve checks are run for this demonstration; in a real project, scope sentence-punctuation checks to instructions and code-sensitive checks to prose. JSON quoting preserves spaces and makes these same rows executable fixtures.

| Candidate target | Matching check IDs | Human decision |
| --- | --- | --- |
| `"Set  the pressure to 1,5bar ."` | `["N02", "S01", "S02"]` | **Correct:** fictional source “Druck auf 1,5 bar einstellen.” confirms the value. Use “Set the pressure to 1.5 bar.” Remove the double space and space before the full stop. N01 misses the comma while the unit is attached; rerun after fixing spacing. |
| `"Set the pressure to 1,5 bar."` | `["N01"]` | **Correct:** with unit spacing fixed, N01 now finds the comma. The same fictional source confirms 1.5 bar; change the separator. |
| `"Use a 15-20 mm spacer."` | `["N03"]` | **Correct:** the source specifies a range, not subtraction. Use “Use a 15–20 mm spacer.” under this house style. |
| `"Check the the valve"` | `["T01", "T02"]` | **Correct:** accidental repetition in a full instruction. Use “Check the valve.” |
| `"Optimize the color display."` | `["L01", "L02"]` | **Correct:** ordinary prose, so use “Optimise the colour display.” This decision comes from the brief, not a universal UK-English rule. |
| `"Use state of the art equipment."` | `["L03"]` | **Correct:** attributive use. Write “Use state-of-the-art equipment.” |
| `"The state of the art is changing."` | `["L03"]` | **Accept:** a noun phrase; hyphenating it would be inappropriate. |
| `"She had had training."` | `["T01"]` | **Accept:** grammatical repetition. |
| `"Installation"` | `["T02"]` | **Accept:** heading; no full stop required. |
| `"CSS color: red;"` | `["L01"]` | **Accept:** code token; changing it to “colour” would break the property name. |
| `"1,234"` | `["N01", "N04", "T02"]` | **Query:** a numeric table cell without its source context. Is this 1.234 or 1234? Do not convert automatically or add sentence punctuation. N04 only selects the cell. |
| `"Wait.."` | `["S03"]` | **Query:** confirm whether this UI string should end with a full stop or an ellipsis; two dots alone do not reveal intent. |
| `"Use a 25 mm spacer."` | `[]` | **Accept after source check:** no listed rule matches. This alone does not prove correctness. |
| `"Open the valve."` | `[]` | **Correct despite no regex finding:** fictional source “Ventil schließen.” means “Close the valve.” Surface checks miss the semantic reversal. |

After correction, rerun QA. An accepted noun phrase or heading can still match; clearing every warning is not the objective. Keep the query rows unresolved until source context or the content owner settles the meaning.
