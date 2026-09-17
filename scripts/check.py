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

allowed_iq = (
    DISC,
    "Train at Brain Camp — puzzles, people sense, trivia. Not an official IQ score.",
    "Not an official IQ score.",
    "not an IQ number",
    "not an IQ score",
)
for path, text in (("index.html", html), ("README.md", readme)):
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"IQ|intelligence quotient", line, re.I):
            stripped = line.strip()
            if any(x in line for x in (
                "selfTest", "iq-words", "iq-as-score", "body.match(/IQ",
                "missing-disc", "iq < 1", "PLAYTEST", "var DISC", "not an IQ number",
            )):
                continue
            if any(a in line for a in allowed_iq):
                continue
            if "DISC" in line and "IQ score" in line:
                continue
            fails.append(f"{path}:{i} unexpected IQ line: {stripped[:120]}")

if html.count('mk("') < 27:
    fails.append("item pool too small")
if "SEED" not in html or "mean: 52" not in html:
    fails.append("missing seed norms")
if "beta seed norms — replace when real cohort exists" not in html:
    fails.append("missing seed comment")
if "visibilitychange" not in html:
    fails.append("missing away handler")
if "bober-brain-camp-v2" not in html:
    fails.append("missing localStorage key")
if "Assess Reasoning" not in html:
    fails.append("missing Assess Reasoning")
if "Assess Memory" not in html:
    fails.append("missing Assess Memory")
if "Assess Speed" not in html:
    fails.append("missing Assess Speed")
if "How we score" not in html:
    fails.append("missing How we score")
if "About scoring" not in html:
    fails.append("missing About scoring")
if "bober-brain-camp-run-v1" not in html:
    fails.append("missing run save key")
if "function ordinal" not in html:
    fails.append("missing ordinal helper")
if 'id="btn-train"' not in html:
    fails.append("missing Train button")
if "EQ · Soon" not in html:
    fails.append("missing EQ Soon")
if "TRAIN_KEY" not in html:
    fails.append("missing train save key")
if "PRACTICE ONLY" not in html:
    fails.append("missing practice-only chip")
if html.count('TQ') < 40:
    fails.append("trivia pool too small")
if re.search(r"connect wallet|wallet connect", html, re.I):
    fails.append("wallet connect string")

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("CHECK_OK")
