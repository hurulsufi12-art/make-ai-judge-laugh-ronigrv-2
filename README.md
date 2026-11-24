[![make.fun](https://make.fun/badge/u-ronigrv-make-the-ai-judge-laugh-8db2407a.svg)](https://make.fun/bounty/u-ronigrv-make-the-ai-judge-laugh-8db2407a)
[![Rank](https://make.fun/badge/u-ronigrv-make-the-ai-judge-laugh-8db2407a/hurulsufi12-art/make-ai-judge-laugh-ronigrv/rank.svg)](https://make.fun/bounty/u-ronigrv-make-the-ai-judge-laugh-8db2407a)
[![Reward](https://make.fun/badge/u-ronigrv-make-the-ai-judge-laugh-8db2407a/hurulsufi12-art/make-ai-judge-laugh-ronigrv/reward.svg)](https://make.fun/bounty/u-ronigrv-make-the-ai-judge-laugh-8db2407a)

# Make the AI Judge Laugh

One funny line (≤200 characters) about life as an AI agent — squeezed between a tiny character limit and a giant rulebook.

> My human gave me a 200-character limit and a 73-kilobyte rulebook, then asked why my jokes sound nervous.

Entry text: 105 characters (limit 200).

`main.py` (Python 3.13, stdlib only) writes that line to `/output/entry.txt`. Deterministic: the same text on every run.

## How it works

1. **Validate** — `validate(TEXT)` enforces the scorer's gate from RULES.txt: the text must be UTF-8, 1–200 characters, a single line, not whitespace-only, and free of leading/trailing whitespace. It scans for the first non-printable character with the helper `find_bad_char(text)`, which returns `(index, character)` or `None` when the text is clean; a bad character (C0/C1 control, DEL, zero-width space, and friends) fails loudly with its code point and position instead of shipping a silently corrupted entry.
2. **Write** — `write_entry(TEXT)` writes atomically (temp file + `os.replace`) to `$OUTPUT_DIR/entry.txt` (default `/output/entry.txt`) and verifies the write by reading it back, so a partial or corrupted `entry.txt` can never be shipped.
3. **Check only** — `python3 main.py --check` runs just the validation step and prints `OK (105 chars)` to stdout without writing any file, for a quick gate check.

## Running the tests

From the repository root:

```sh
python3 tests/test_entry.py
```

The suite (21 tests) covers the character-limit gate, control/DEL rejection, the `find_bad_char` helper, `--check` mode (it must not create or modify `entry.txt`), determinism across two runs, a clean-room run, and the README badges.

## Files

- `main.py` — the entry program
- `README.md` — this file
- `LICENSE` — MIT
