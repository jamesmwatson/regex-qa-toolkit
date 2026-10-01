# Portfolio revision work log

## Scope and provenance

Reviewed the complete original repository: README, five pattern text files and one sample-string file. Also reviewed the supplied translator canvas and earlier generated workflow suggestions. The latter are candidate material, not evidence that a check was deployed professionally. No private notes, source/client examples or chat exports are included in this repository.

The revised scope is twelve documented checks in four categories, two workflow/example pages and a small standard-library test runner. It retains useful original checks and fictional fixtures, replacing the unexplained text files rather than maintaining two competing catalogues.

## Selected checks

| IDs | Why include them? |
| --- | --- |
| S01–S02 | Common, easily recognisable formatting candidates; demonstrate horizontal versus line-breaking whitespace and why English punctuation assumptions matter. |
| S03 | Small punctuation check with clear boundaries, useful non-matches and a concrete repair. |
| N01–N03 | Technical-translation examples that require both numerical caution and a project style decision: decimal punctuation, unit spacing and ranges. |
| N04 | Shows that regex can select material for review without labelling it erroneous. |
| T01 | Demonstrates a useful backreference and grammatical false positives. |
| T02 | Makes content-type scoping visible: full sentences versus headings and UI labels. |
| L01–L03 | Shows lexical consistency, explicit house-style assumptions and a case where syntax alone cannot justify a replacement. |

## Repairs and narrowed claims

- **Whitespace:** narrowed the original broad whitespace classes to explicit horizontal characters, preserving line breaks and making NBSP behaviour visible. Space-before-punctuation is explicitly English-scoped.
- **Two dots:** the original expression consumed neighbouring characters and missed `Done..`. S03 uses fixed-width boundary assertions, returns only the two dots and excludes three-dot ellipses.
- **Numeric candidates:** replaced broad substring detection and the “European” locale label with explicit scope. N01 accepts terminal sentence punctuation, avoids matching inside identifiers and excludes mixed/grouped separator forms. The latter are coverage gaps, not validated numbers.
- **Check interaction:** the first worked-example test exposed that N01 excludes a number attached to a unit. N02 catches `1,5bar`; after inserting the space, N01 can find the comma. Added an explicit negative fixture and a second-pass example rather than claiming broader coverage.
- **Ranges / units:** retained the practical ideas but defined a small, case-sensitive unit list. Removed unsupported claims about universally correct dash spacing and non-breaking characters. Signed ranges remain outside N03's scope.
- **Repeated words:** narrowed generic word characters to unaccented English letter tokens and horizontal separators. Grammatical repetition is tested as an expected, acceptable match.
- **Spelling:** replaced broad suffix conversion with a small word-family allowlist. The original conversion produced `sise`, `prise` and `capsise` from `size`, `prize` and `capsize` in a Python diagnostic. The new rule flags for review and does not assert that all UK English requires `-ise`.
- **Contextual phrase:** removed the claim that a following word establishes attributive use. The noun phrase in “The state of the art is changing” matches intentionally and must be accepted.
- **Workflow claims:** removed blanket statements about auto-propagation requiring completely identical segments and about global replacements being safe. Regex detection, native verification, propagation and replacement have distinct roles.

## Rejected or deferred candidates

| Candidate | Decision and evidence |
| --- | --- |
| Grouped-number conversion containing `(1, 3)` and a digit-class token followed by literal `3` | Rejected as written: the suggested expression did not match `1,234.56`. Parentheses group text; `{1,3}` is a quantifier. Correcting syntax alone would not safely swap decimal and grouping separators. No automatic conversion recipe retained. |
| Broad international phone-number replacement | Rejected: malformed pseudo-quantifiers, incomplete capture groups for the proposed replacement and country-specific numbering assumptions. Outside the compact QA scope. |
| “Placeholder not preserved” | Removed: the old expression matched the last existing numeric placeholder, and found nothing when none was present. Missing placeholders require source–target comparison, including identity/count/order as relevant. |
| “Non-breaking space before punctuation” | Removed: the old rule produced a zero-width match after punctuation, including on `Ready!`; it did not check the claimed position. A specific French typography requirement would need its own scoped rule. |
| Sentence-start capitalisation, mid-sentence capitals and “shouting” | Deferred: abbreviations, proper names, product codes, headings and sentence boundaries create substantial noise. The original sentence-start lookbehind also failed to compile in Python because its alternatives had different widths; no cross-engine claim retained. |
| Generic missing space after punctuation; mixed/doubled punctuation | Deferred: decimals, URLs, abbreviations and stylistic punctuation need more scoping. Retained the narrower two-dot check. |
| Decimal-point-as-“European”-error, long digit runs, mixed separators | Removed as general error claims: locale cannot be inferred from a continental label; codes, grouping and decimals can legitimately coexist. N01 covers a narrower question. |
| Trailing whitespace, double hyphens and straight-quote conversion | Deferred to avoid a general cleanup catalogue. Intended typography, markup and content type determine the action. |
| “Mixed languages” from Latin/Cyrillic characters | Removed: mixed scripts do not establish mixed languages or an error. A scoped confusable-character check would be a different task. |
| Regex tag stripping | Removed: markup/tag integrity belongs to format-aware tooling. Stripping apparent tags can destroy localisation structure. |
| Comma-separated lists without final punctuation | Deferred: useful as a filter in a specified workflow, but lists can legitimately lack punctuation and comma-decimal values complicate selection. N04 already demonstrates triage; T02 demonstrates content-type limits. |
| Number–hyphen–abbreviated-unit pattern from notes | Replaced conceptually by N02's explicit missing-space check. The notes' one/two-letter rule can match only the tail of a number and arbitrary letter tokens; it does not establish whether a compound modifier needs a hyphen. |
| Case/spacing conversion for “e-commerce” | Rejected as a general replacement: the earlier proposed spacing was unjustified and the casing coverage was overstated. An approved product term should be handled against its actual specification. |

## Validation and recruiter review

- All **12** expressions compiled and passed **94** exact-span fixtures in Python **3.12.14**.
- All **14** worked-example rows passed against all checks: **168** rule evaluations, including unexpected-match detection.
- The runner reads the displayed expressions and examples directly, so the documentation is the tested source.
- The README opens with practical problems, workflow placement and the human decision. It identifies the author's translation/review background without claiming that every check was used professionally.
- The worked review demonstrates correction, acceptance, escalation, interactions between checks and a semantic error that regex misses. No accuracy, productivity or deployment statistics are claimed.

The main remaining gap is a small end-to-end run in an actual CAT-tool project. A later session could verify these fixtures in the user's Trados version, document flag/tag behaviour and add one fictional screenshot. A labelled synthetic bilingual set could then test a specific source–target requirement such as placeholder preservation. Neither requires expanding this into an application or a much larger pattern catalogue.
