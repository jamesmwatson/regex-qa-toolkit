# Regex QA Toolkit

I built this toolkit around a problem I ran into repeatedly as a translator and reviewer: the same small QA issue can crop up in dozens of completely different segments.

A regex can pull those cases together: `25mm`, a decimal comma in an English target or an accidental `the the`. It's much faster than checking them one by one. It can't tell you that every match is wrong, though. The useful part is combining pattern matching with the source text, the project style and linguistic judgement.

I worked mainly on technical and commercial German-to-English material, so the examples here lean towards measurements, numbers, punctuation and English usage. Some checks grew out of working notes and earlier QA patterns; others are small examples I've added to demonstrate the same approach. All sample content is fictional.

## Checks in action

![Regex QA running in Trados Studio](/screenshots/trados-regex-qa-overview.png)
Selected regex checks running in Trados Studio 2019 QA Checker 3.0 on a fictional DE→EN technical project. Findings include measurement formatting, repeated whitespace and language-level review candidates.

![A match still needs judgement](/screenshots/trados-regex-human-review.png)
Two findings from the same QA pass: `the the` is an accidental repetition, while `state of the art` is correct here as a noun phrase and is deliberately accepted. A regex match is a review candidate, not automatically an error.


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

## Why use regex for QA

I worked for around ten years as a professional translator and reviewer, mainly on technical and commercial German-to-English material. Regex was one of the practical tools I used to find recurring formatting, numerical, terminology and text-quality issues in CAT-tool workflows.

A measurement can recur with a different value in every segment; a small punctuation problem can be scattered through product descriptions. A focused query brings those instances together for review. Useful QA also means knowing when to leave a match alone: a product name, a code token, a valid thousands separator or a grammatical repetition.

This repository turns that background into a small, documented portfolio collection. The collection mixes patterns adapted from my own working notes and earlier toolkit with examples developed specifically for this portfolio. All sample content is fictional and no client material is included.

## Using the checks

Copy a check into a regex-capable CAT tool or text editor. Trados is one relevant environment but you don't need a CAT tool to use these checks or find them useful. Regex is supported in a surprising number of editors and other text-processing tools, so the same habits transfer quite well.

The expressions and documented examples are exercised directly by a small Python standard-library script:

```sh
python3 tests/run_tests.py
```
Selected checks have also been run successfully in Trados Studio 2019 QA Checker 3.0 against the fictional DE→EN project shown above.

## Limits that affect review

- **Shape is not meaning.** `1,234` can be correct English grouping. A number can have perfect formatting and the wrong value. Check against the source.
- **Language and content type matter.** English punctuation rules do not transfer unchanged to French; headings and UI labels may need no full stop; UK English does not imply a universal `-ise` rule.
- **Text checks cannot see everything.** Tags, placeholders, source–target omissions and cross-segment terminology require appropriate native QA, comparison or human review. Do not strip tags to make a regex work.
- **Coverage is deliberately narrow.** ASCII digits, selected units and English word forms are documented choices. A non-match means only that this particular check found nothing. These checks can assist human or AI-generated translation review, but cannot assess overall translation quality.