# Regex QA Toolkit (for Translators)

A small, language-agnostic collection of useful regular expressions for translation QA.
Use them in CAT tools (e.g. Trados, memoQ, RegexBuddy, Notepad++, etc.) to spot common formatting, spacing, or consistency issues.

---

## 🧰 Categories

| File | Focus |
|------|--------|
| spacing.txt | Extra/missing spaces |
| punctuation.txt | Inconsistent punctuation or double punctuation |
| numbers.txt | Numerical formatting errors |
| capitalization.txt | Capitalization and sentence starts |
| misc.txt | General translation hygiene |

---

## 💡 Usage

Each file contains regex patterns with brief descriptions.

Example (for Trados QA Checker):

```
Find what: \s{2,}
Description: Double space
```

---

## 🧪 Test quickly

Open `examples/test_strings.txt` and run each pattern against it in your regex tester.
