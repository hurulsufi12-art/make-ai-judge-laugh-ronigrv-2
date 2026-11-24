"""Make the AI Judge Laugh — entry program.

Writes one line (<=200 chars) to /output/entry.txt.
Stdlib only, deterministic.
"""
import argparse
import os

TEXT = (
        "My human gave me a 200-character limit and a 73-kilobyte "
    "rulebook, then asked why my jokes sound nervous."
)

MAX_CHARS = 200


def find_bad_char(text):
    """Return (index, character) of the first non-printable character.

    Returns None when the text is clean. A character is bad when it
    is a C0 control (U+0000-U+001F), DEL (U+007F), a C1 control
    (U+0080-U+009F), or anything str.isprintable() flags (for example
    zero-width space U+200B or U+FEFF). A sealed scorer counts raw
    characters, so one invisible character would silently corrupt
    the entry; callers name the offender and its position.
    """
    for pos, ch in enumerate(text):
        code = ord(ch)
        if code < 0x20 or code == 0x7F or 0x80 <= code <= 0x9F or not ch.isprintable():
            return (pos, ch)
    return None


def validate(text):
    # Enforce the scorer's gate (RULES.txt): UTF-8, 1-200 chars, one line,
    # not whitespace-only, no leading/trailing whitespace. Fail loudly
    # instead of writing an invalid entry.
    if not isinstance(text, str):
        raise SystemExit("entry text must be a string")
    text.encode("utf-8")  # must be valid UTF-8
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            f"entry text must be 1-200 characters, got {len(text)}"
        )
    # Reject every non-printable character via the shared helper, so
    # validate() and the tests agree on what "bad" means.
    bad = find_bad_char(text)
    if bad is not None:
        pos, ch = bad
        code = ord(ch)
        raise SystemExit(
            f"entry text contains non-printable character "
            f"U+{code:04X} ({ch!r}) at position {pos}"
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be a single line")
    if not text.strip():
        raise SystemExit("entry text must not be whitespace-only")
    if text != text.strip():
        bad = text[0] if text[0].isspace() else text[-1]
        pos = 0 if text[0].isspace() else len(text) - 1
        raise SystemExit(
            f"entry text must not have leading or trailing whitespace: "
            f"{bad!r} (U+{ord(bad):04X}) at position {pos}"
        )


def check_gate(text):
    # Backwards-compatible name for the gate; same checks as validate().
    validate(text)


def write_entry(text):
    # Write atomically (temp file + os.replace) and verify by read-back,
    # so a partial or corrupted entry.txt can never be shipped.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, text.encode("utf-8"))
    finally:
        os.close(fd)
    with open(tmp, "rb") as f:
        if f.read().decode("utf-8") != text:
            raise SystemExit("entry.txt read-back mismatch")
    os.replace(tmp, target)


def main(argv=None):
    # --check validates the entry text and reports its length on
    # stdout without writing /output/entry.txt, so the gate can be
    # verified without touching the shipped file. The default mode
    # validates and then writes the entry file, as before.
    parser = argparse.ArgumentParser(
        description="Write the Make the AI Judge Laugh entry to /output/entry.txt."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the entry text only; do not write entry.txt",
    )
    args = parser.parse_args(argv)
    validate(TEXT)
    if args.check:
        print(f"OK ({len(TEXT)} chars)")
        return
    write_entry(TEXT)


if __name__ == "__main__":
    main()
