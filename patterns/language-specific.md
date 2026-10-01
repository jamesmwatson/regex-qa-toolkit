# English and locale-specific checks

I’d use these checks to review English spelling and phrasing against a project’s house style. The useful question is whether a form is right for this text, rather than whether one variant is always better than another.

The examples below double as test fixtures. JSON strings make invisible characters visible; `[]` means the pattern should not match.

[Toolkit overview](../README.md) · [Test conventions](../tests/test-cases.md)

## L01 — Color / colour inventory

```regex
(?i)\bcolou?r\b
```

**What it catches:** Both `color` and `colour`, so their use can be reviewed together.

**When I'd use it:** When checking spelling consistency in an English project, especially material assembled from sources using different English variants.

**Watch out for:** Either spelling may be correct. Code, product names and quoted UI labels may need to retain `color` even in UK English prose. The check ignores case and finds the words on their own or in hyphenated forms such as `color-coded`; plurals such as `colors` and joined forms such as `discoloration` are outside its scope.

**If found:** Compare the wording with the project’s preferred spelling and the kind of content. I’d correct ordinary prose where needed, while preserving code and official names or labels.

| Input | Expected matches | Review note |
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

**What it catches:** Selected spellings such as `optimize`, `localization` and `customized` that may need an `s` under the project’s house style.

**When I'd use it:** When a project explicitly asks for `-ise` and `-isation` spellings, rather than assuming that requirement from a UK English language setting.

**Watch out for:** Some UK styles accept or prefer `-ize`. I’ve kept this check to selected forms of `organise`, `localise`, `optimise` and `customise`, avoiding unrelated words such as `size` and `prize`. It ignores case, but doesn’t check whether every matched form is a valid word or whether it belongs to a protected name.

**If found:** Check the house style and context, then change the spelling where appropriate. I’d preserve the existing capitalisation, leave official names alone and review words individually rather than make a general `z-to-s` replacement.

| Input | Expected matches | Review note |
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

**What it catches:** The phrase `state of the art` written without hyphens.

**When I'd use it:** In technical or marketing copy where I want to check whether the phrase needs hyphenating before a noun, as in `state-of-the-art equipment`.

**Watch out for:** `The state of the art is changing` is already correct. Another word following the phrase doesn’t by itself tell me how the phrase is being used. The check ignores case and allows spaces or tabs between the words, but doesn’t cross line breaks.

**If found:** Read the whole phrase. I’d hyphenate an attributive use such as `state-of-the-art equipment` where the house style calls for it, and leave the noun phrase `the state of the art` unchanged.

| Input | Expected matches | Review note |
| --- | --- | --- |
| `"Use state of the art equipment."` | `["state of the art"]` | Candidate attributive phrase. |
| `"STATE OF THE ART equipment"` | `["STATE OF THE ART"]` | Case-insensitive. |
| `"Use state-of-the-art equipment."` | `[]` | Useful non-match: already hyphenated. |
| `"The state of the art is changing."` | `["state of the art"]` | Known acceptable noun phrase. |
| `"state of the artist"` | `[]` | Whole-word boundary. |
| `"state\nof the art"` | `[]` | No cross-line match. |