#!/usr/bin/env python3
"""Check the regex and worked-example fixtures embedded in the Markdown docs."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECK_HEADING = re.compile(r'^## ([A-Z][0-9]{2}) — .+$', re.MULTILINE)
# The two code spans contain JSON; the final prose cell is for human readers.
FIXTURE_ROW = re.compile(r'^\| `([^`]+)` \| `([^`]+)` \| .+ \|$', re.MULTILINE)


def fixtures(text):
    for row in FIXTURE_ROW.finditer(text):
        value, expected = (json.loads(cell) for cell in row.groups())
        if not isinstance(value, str) or not isinstance(expected, list):
            raise ValueError('Fixture input must be a string; expectation must be a list.')
        if not all(isinstance(item, str) for item in expected):
            raise ValueError('Expected match lists must contain strings.')
        yield value, expected


def main():
    patterns = {}
    failures = []
    pattern_cases = 0
    for path in sorted((ROOT / 'patterns').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        headings = list(CHECK_HEADING.finditer(text))
        if not headings:
            raise ValueError(f'No checks found in {path.name}')
        for index, heading in enumerate(headings):
            check_id = heading.group(1)
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            section = text[heading.end():end]
            blocks = re.findall(r'```regex\n([^\n]+)\n```', section)
            if len(blocks) != 1 or check_id in patterns:
                raise ValueError(f'{check_id}: require one expression and a unique ID')
            regex = re.compile(blocks[0])
            patterns[check_id] = regex
            cases = list(fixtures(section))
            if not any(expected for _, expected in cases) or not any(not expected for _, expected in cases):
                raise ValueError(f'{check_id}: require positive and negative examples')
            for value, expected in cases:
                actual = [match.group(0) for match in regex.finditer(value)]
                pattern_cases += 1
                if actual != expected:
                    failures.append(f'{check_id}: {value!r}: expected {expected!r}, got {actual!r}')
    expected_ids = {'S01', 'S02', 'S03', 'N01', 'N02', 'N03', 'N04', 'T01', 'T02', 'L01', 'L02', 'L03'}
    if set(patterns) != expected_ids:
        raise ValueError(f'Unexpected check inventory: {sorted(patterns)}')
    worked_text = (ROOT / 'examples' / 'sample-qa-results.md').read_text(encoding='utf-8')
    worked_cases = list(fixtures(worked_text))
    if not worked_cases:
        raise ValueError('No worked-example fixtures found')
    for value, expected in worked_cases:
        actual = sorted(check_id for check_id, regex in patterns.items() if regex.search(value))
        if actual != sorted(expected):
            failures.append(f'Worked example: {value!r}: expected {expected!r}, got {actual!r}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'PASS: {len(patterns)} checks; {pattern_cases} pattern fixtures; '
          f'{len(worked_cases)} worked-example rows ({len(patterns) * len(worked_cases)} rule evaluations).')
    print(f'Engine: Python {sys.version.split()[0]} re. CAT-tool integration not tested.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
