# Applying a check in a CAT workflow

[Overview](../README.md) · [Worked example](sample-qa-results.md)

## Prepare a focused review

1. Establish the source and target locales, the project style and the content type. For example: German source, UK English target, technical instructions, decimal points and spaces before unit symbols.
2. Run the tool's relevant built-in number, tag, terminology and punctuation checks. Add a regex only where its scope or explanation helps; avoid duplicating noisy warnings.
3. Select one documented check. Read its assumptions and copy its positive, negative and acceptable-match examples into a small scratch document first.
4. Set the intended target-side scope. Use regex search or a filter to gather candidates, or configure a QA rule that reports a target match. These are different operations: filtering is not correction.
5. Inspect each finding alongside the source and surrounding content. Record **correct**, **accept** or **query**, with a short reason where needed. For an ambiguous value, query it rather than guessing.
6. Correct confirmed issues, then rerun the same check and native QA. Retained matches may be justified exceptions. Inspect the final rendered/exported material for layout and tag effects.

## Trados example

Trados Studio offers regex rules in **QA Checker 3.0 → Regular Expressions**. In the project's verification settings, add a descriptive rule such as `S02 — whitespace before English punctuation`, paste the expression from [S02](../patterns/spacing-and-punctuation.md#s02--whitespace-before-english-punctuation) and configure it to report matches in the target. Exact controls vary by version; check the project's settings rather than assuming global defaults apply.

Alternatively, use the editor's regex-capable search/filter for an ad hoc review. Do not assume a search field and a verifier treat tags, segments or flags identically. Keep multiline off for these segment-level examples; retain the inline case flag where supplied and do not enable ignore-case for unit checks.

First confirm the scratch fixtures behave as documented. Then run the rule on a small selection of relevant content before applying it more broadly. This repository has not been integration-tested inside Studio; Python test results do not establish Studio behaviour.

Auto-propagation and regex serve different purposes. Propagation reuses translations for matching or similar source content under the tool's settings. Regex locates a textual shape across otherwise different strings. Do not assume changes in numbers always prevent propagation, or that regex must replace functionality the CAT tool already provides.

## Replacement is a separate decision

For a confirmed plain-prose double space, replacing the selected run with one ordinary space may be reasonable. A decimal separator, word spelling or range requires more context. Begin with individual corrections; only use a bulk operation when the reviewed scope has a single justified transformation, a recoverable copy and a checked output.

Replacement syntax is tool-specific: a capture reference in a pattern is not necessarily written the same way in a replacement field. This toolkit deliberately supplies detection patterns and human decisions, not portable replacement recipes. Never apply the patterns directly to raw bilingual XML or strip markup as a shortcut.

## References

- RWS: [Specifying regular expressions for QA Checker](https://docs.rws.com/sdl-trados-studio-783545/specifying-regular-expressions-for-qa-checker-345947).
- RWS: [Auto-propagation](https://docs.rws.com/en-US/trados-studio-2024-sr1-1187677/auto-propagation-353178).
- Microsoft: [.NET regex character classes](https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-classes-in-regular-expressions) explains why shorthand classes such as word characters and whitespace need careful interpretation.
