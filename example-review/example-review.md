# Worked example: a fictional technical review

## Project brief

This fictional project uses UK English. The house style calls for:

- decimal points for decimals;
- a space between values and unit symbols;
- en dashes for closed numerical ranges;
- selected `-ise` spellings;
- `colour` in ordinary prose, while software/code terms are preserved exactly;
- final punctuation for complete instructions, but not for headings or short UI labels.

The source text and target examples below are all fictional. I deliberately introduced a mixture of genuine errors, acceptable matches and one semantic mistranslation to show what regex QA can and cannot help with.

## Review

| German source | English target | Finding | Decision |
| --- | --- | --- | --- |
| `Vor der Inbetriebnahme das Zulaufventil schließen und die Pumpe auf sichtbare Schäden prüfen.` | `Before commissioning, open the inlet valve and check the pump for visible damage.` | None | **Correct:** this reverses the meaning of `schließen` (“close”). None of these surface-pattern checks detects the semantic error. |
| `Zwischen Pumpengehäuse und Seitenwand einen Abstand von 15–20 mm einhalten.` | `Maintain a clearance of 15-20 mm between the pump housing and the side wall.` | `N03` | **Correct:** the project style uses an en dash for a closed numerical range, so use `15–20 mm`. |
| `Der Schlauch darf nicht geknickt oder unter Spannung montiert werden.` | `The hose must not be kinked or installed under tension.` | None | **Accept:** no listed regex check matches, and the target is suitable after source review. |
| `Förderdruck: 1,5 bar` | `Delivery pressure: 1,5bar` | `N02`, then `N01` | **Correct:** first add the missing space before `bar`. Once separated, the decimal-comma check can flag `1,5`; under this house style the final form is `1.5 bar`. |
| `Max. Schlauchlänge: 25 mm` | `Max. hose length: 25mm` | `N02` | **Correct:** insert the required space between the value and unit. |
| `Temperaturbereich: 5–40 °C` | `Temperature range: 5-40 °C` | `N03` | **Correct:** replace the ASCII hyphen with the project’s en dash. |
| `Drücken Sie zweimal die Taste START, um die Entlüftung zu beginnen.` | `Press  the START button twice to begin priming .` | `S01`, `S02` | **Correct:** remove the accidental double space and the space before the full stop. |
| `Optimieren Sie bei Bedarf die Anzeige für die aktuelle Anwendung.` | `Optimize the display for the current application if necessary.` | `L02` | **Correct:** this project calls for the selected `-ise` spelling, so use `Optimise`. |
| `Die Farbe der Statusanzeige kann im Menü „Display“ geändert werden.` | `The status indicator color can be changed in the Display menu.` | `L01` | **Correct:** this is ordinary prose, so the project style calls for `colour`. |
| `Warten..` | `Wait..` | `S03` | **Correct:** under this fictional style, short UI labels take no final punctuation, so use `Wait`. |
| `Der Filter ist nach jeweils 500 Betriebsstunden zu prüfen.` | `Check the the filter every 500 operating hours.` | `T01` | **Correct:** remove the accidental repeated word. |
| `Der aktuelle Stand der Technik ist bei allen Wartungsarbeiten zu berücksichtigen.` | `The state of the art must be considered during all maintenance work.` | `L03` | **Accept:** `state of the art` is a noun phrase here, so hyphenating it would be inappropriate. |
| `Installation` | `Installation` | `T02` | **Accept:** this is a heading, and the project style does not require final punctuation. |
| `1,234` | `1,234` | `N01`, `N04`, `T02` | **Review:** without more context, this could represent different values under different numeric conventions. Do not convert it automatically or treat it as sentence text just because other checks also match. |

## What this shows

The useful outcome is not a warning-free file. Some matches are genuine errors, some are acceptable in context, and some need more information before a decision can be made.

The opposite also matters: a segment can pass every regex check and still be wrong. The `schließen` → `open` example is a semantic mistranslation that surface-pattern QA will not catch.

That is why I use regex as a way to gather review candidates, not as a substitute for reading the source, applying the project style and making a linguistic judgement.
