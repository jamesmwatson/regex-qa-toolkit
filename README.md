# Regex QA Toolkit

A production-informed toolkit of regex-based QA checks for translation and localisation workflows. The checks target recurring formatting, numerical, punctuation and linguistic issues and surface **candidates for human review**.

In technical translation, different sentences can share the same small problem: `25mm`, an English target containing `12,5`, or an accidental `the the`. Regex makes those recurring shapes searchable across otherwise different segments. The reviewer still decides whether a match is wrong, what the source means and which locale or house style applies.

**Workflow:** translate or post-edit → run native CAT-tool QA plus selected regex checks → inspect source, target and context → correct or accept each finding → rerun QA.

## Start here

- **[Worked QA review](examples/sample-qa-results.md):** fictional technical strings, findings and human decisions—including acceptable matches and a missed mistranslation.
- **[CAT / Trados workflow](examples/trados-workflow.md):** select a rule, test it, review findings and recheck changes.
- **[Test cases and validation](tests/test-cases.md):** reproducible positive examples, non-matches and known limitations.

| Checks | Practical purpose |
| --- | --- |
| [Numbers and measurements](patterns/numbers-and-measurements.md) | Review decimal-comma candidates, unit spacing and hyphenated ranges; filter simple numeric-only segments. |
| [Spacing and punctuation](patterns/spacing-and-punctuation.md) | Find repeated horizontal whitespace, spaces before English punctuation and exactly two full stops. |
| [Text and consistency](patterns/text-and-consistency.md) | Review repeated words and possible missing final punctuation in sentence-like content. |
| [English / locale-specific](patterns/language-specific.md) | Inventory `color/colour`, check selected `-ize` forms against an `-ise` house style and review `state of the art` in context. |

## Why this existed in practice

I worked for around ten years as a professional translator and reviewer, mainly on technical and commercial German-to-English material. Regex was one of the practical tools I used to find recurring formatting, numerical, terminology and text-quality issues in CAT-tool workflows.

A measurement can recur with a different value in every segment; a small punctuation problem can be scattered through product descriptions. A focused query brings those instances together for review. Useful QA also means knowing when to leave a match alone: a product name, a code token, a valid thousands separator or a grammatical repetition.

This repository turns that background into a small, documented portfolio collection. **Production-informed describes the problem selection and review approach; it does not mean every expression here was deployed in paid work.** Individual checks identify whether they were adapted from the original collection, translator notes or generated candidate suggestions, or written as illustrative examples. All examples are fictional; no client material is included.

## Using the checks

Copy a check into a regex-capable CAT tool, text editor or segment-processing workflow. Trados is one relevant environment; no CAT tool is required to read or use the collection. Start with the project's source/target locales, content types and style guide, then enable only relevant checks. A colour inventory or numeric filter selects material; it does not assert an error.

The expressions and documented examples are exercised directly by a small Python standard-library script:

```sh
python3 tests/run_tests.py
```

Python is optional for using the patterns. There are no third-party dependencies, application or automatic replacements. Validation here covers Python's regex engine; repeat the examples in your actual CAT tool before relying on its flags, boundaries or tag handling.

## Limits that affect review

- **Shape is not meaning.** `1,234` can be correct English grouping. A number can have perfect formatting and the wrong value. Check against the source.
- **Language and content type matter.** English punctuation rules do not transfer unchanged to French; headings and UI labels may need no full stop; UK English does not imply a universal `-ise` rule.
- **Text checks cannot see everything.** Tags, placeholders, source–target omissions and cross-segment terminology require appropriate native QA, comparison or human review. Do not strip tags to make a regex work.
- **Coverage is deliberately narrow.** ASCII digits, selected units and English word forms are documented choices. A non-match means only that this particular check found nothing. These checks can assist human or AI-generated translation review, but cannot assess overall translation quality.

See the [work log](WORK_LOG.md) for selection decisions, repairs and rejected candidates.
