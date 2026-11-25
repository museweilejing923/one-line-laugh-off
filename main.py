"""A raccoon, a phone, and 3 a.m.: one cold-read laugh, checked and printed."""

import string
import sys
import unicodedata
from pathlib import Path

ENTRY = "I told my phone I was going to bed early. It showed me a video of a raccoon washing cotton candy, and now it is 3 a.m."
MAX_LEN = 200
CLOSERS = ".!?"
OUT_PATH = Path("/output/entry.txt")


class EntryError(Exception):
    """One of the entry rules was broken."""


class EntryChecker:
    """Validates the fixed entry in three passes: shape, wording, topic."""

    def __init__(self, sentence):
        self.sentence = sentence

    def run(self):
        self._shape_pass()
        self._wording_pass()
        self._topic_pass()
        self._fresh_pass()

    def _fresh_pass(self):
        # A one-liner must not lean on a hyphen at either edge: a
        # leading or trailing "-" reads like a cut-off fragment.
        text = self.sentence
        if text.startswith("-") or text.endswith("-"):
            raise EntryError("must not start or end with a hyphen")

    def _shape_pass(self):
        text = self.sentence
        if len(text) > MAX_LEN:
            raise EntryError("over %d characters" % MAX_LEN)
        if not text.strip():
            raise EntryError("blank entry")
        if any(unicodedata.category(ch) == "Cc" for ch in text):
            raise EntryError("control character found")
        if text.strip() != text or "  " in text or "\n" in text or "\r" in text:
            raise EntryError("ragged edges, double space, or line break")
        if not text or text[-1] not in CLOSERS:
            raise EntryError("must end with . ! or ?")

    def _wording_pass(self):
        text = self.sentence
        letters = [ch for ch in text if ch.isalpha()]
        if text and all(ch in string.punctuation for ch in text):
            raise EntryError("punctuation only")
        if text.isdigit():
            raise EntryError("digits only")
        if not letters:
            raise EntryError("no letters")
        if any(a == b == c for a, b, c in zip(text, text[1:], text[2:])):
            raise EntryError("one character repeated three times in a row")
        if "---" in text:
            raise EntryError("triple hyphen is not a sentence")

    def _topic_pass(self):
        if "raccoon" not in self.sentence.casefold():
            raise EntryError("must mention the raccoon")


def emit():
    try:
        EntryChecker(ENTRY).run()
    except EntryError as problem:
        sys.stderr.write("invalid: %s\n" % problem)
        raise SystemExit(1)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    emit()
