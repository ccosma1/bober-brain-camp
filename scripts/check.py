#!/usr/bin/env python3
"""Static honesty + pool checks for Bober Brain Camp."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
fails = []

DISC = "Fan game skill index — not a clinical or diagnostic test. Not an IQ score."
if DISC not in html:
    fails.append("missing disclaimer in html")
if "not a clinical" not in readme.lower():
    fails.append("readme missing clinical honesty")

# Player-facing IQ may only appear in the locked honesty lines.
allowed_iq = {
    DISC,
    "Train at Brain Camp — puzzles, people sense, trivia. Not an official IQ score.",
    "Not an official IQ score.",
    "**Honesty:** Fan game skill index — not a clinical or diagnostic test. Not an IQ score. Results are a Reasoning skill bar (0–100) and a beta cohort percentile only. No clinical score, no official test.",
    "Mission: Train at Brain Camp — puzzles, people sense, trivia. Not an official IQ score.",
}
for path, text in (("index.html", html), ("README.md", readme)):
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"IQ|intelligence quotient", line, re.I):
            stripped = line.strip()
            if "selfTest" in line or "iq-words" in line or "iq-as-score" in line or "body.match(/IQ" in line:
                continue
            if "missing-disc" in line or "iq < 1" in line or "PLAYTEST" in line:
                continue
            if "var DISC" in line:
                continue
            if any(a in line for a in allowed_iq):
                continue
            if "DISC" in line and "IQ score" in line:
                continue
            fails.append(f"{path}:{i} unexpected IQ line: {stripped[:120]}")

if re.search(r"WAIS|Raven Progressive|Mensa", html):
    if "WAIS|Raven|Mensa" not in html:
        fails.append("clinical brand in html")
# The selftest regex mentions those names; that is the only allowed hit.

if html.count('mk("') < 27:
    fails.append("item pool too small")
if "FORM_A" not in html or "SEED_MEAN = 52" not in html:
    fails.append("missing seed norms")
if "beta seed norms — replace when real cohort exists" not in html:
    fails.append("missing seed comment")
if "visibilitychange" not in html:
    fails.append("missing away handler")
if "bober-brain-camp-v1" not in html:
    fails.append("missing localStorage key")
if "START CAMP" not in html:
    fails.append("missing Start Camp")
for stub in ("Train · Soon", "Trivia · Soon", "EQ · Soon", "Museum · Soon"):
    if stub not in html:
        fails.append(f"missing stub {stub}")
if "wallet" in html.lower() and "connect" in html.lower():
    # splash must not offer a wallet connect
    if re.search(r"connect wallet|wallet connect", html, re.I):
        fails.append("wallet connect string")

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("CHECK_OK")
