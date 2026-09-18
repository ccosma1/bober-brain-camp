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
    "Skill facets inside Brain Camp — not a clinical or certified IQ test.",
    "not a clinical or certified IQ test",
    "not a clinical score, not an IQ number, not certified.",
)
for path, text in (("index.html", html), ("README.md", readme)):
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"\bIQ\b|intelligence quotient", line, re.I):
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

if "Row March" not in html or "Beaver Orbit" not in html:
    fails.append("missing reasoning families")
if "FORM_NAMES" not in html or "FORM_F" not in html:
    fails.append("missing forms A-F")
if "MEM_PACKS" not in html:
    fails.append("missing memory packs")
if "SPEED_TEMPLATES" not in html:
    fails.append("missing speed templates")
if "Skill facets inside Brain Camp — not a clinical or certified IQ test." not in html:
    fails.append("missing facet honesty line")
if "What these skills can be useful for" not in html:
    fails.append("missing usefulness section")
for i, line in enumerate(html.splitlines(), 1):
    if ("TAP WHAT CHANGED" in line or "fill-the-gap" in line) and "fails.push" not in line and "mem-change" not in line:
        fails.append(f"index.html:{i} memory change/gap copy still present")
        break
if "Lodge Dinner" not in html:
    fails.append("missing Lodge Dinner museum card")
if "assets/teach/quantum.jpg" not in html or "assets/teach/steam.jpg" not in html:
    fails.append("missing trivia teach graphs")
if "Quantum Step" not in html or "Thermo · Steam" not in html or "Snow Insulates" not in html:
    fails.append("missing museum teach-graph cards")
if "What skills are useful for" not in html:
    fails.append("missing museum useful-for card")
if "assets/museum/useful.jpg" not in html:
    fails.append("missing unique useful-for thumb")
if "Beta norms (early). Assess bars stay separate. Social Read is practice only." in html.split('<div id="profile"')[1].split('<div id="museum"')[0]:
    fails.append("beta-norms wall still on Profile")
if "About this skill" not in html:
    fails.append("missing About this skill")
if html.count("Often helps with") < 4:
    fails.append("missing often-helps copy")
if re.search(r"\bADHD\b", html):
    for i, line in enumerate(html.splitlines(), 1):
        if re.search(r"\bADHD\b", line) and "fails.push" not in line:
            fails.append(f"index.html:{i} ADHD in UI")
            break
if re.search(r"\b(Raven|WAIS|SPM|RPM|Mensa)\b", html):
    for i, line in enumerate(html.splitlines(), 1):
        if re.search(r"\b(Raven|WAIS|SPM|RPM|Mensa)\b", line) and "fails.push" not in line and "brand-" not in line:
            fails.append(f"index.html:{i} brand test name in UI")
            break
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
if html.count("<summary>How scored</summary>") > 0:
    fails.append("How scored accordion should be gone")
if html.count('data-about') > 8:
    fails.append("too many About scoring controls")
if "About scoring" not in html:
    fails.append("missing About scoring")
if "bober-brain-camp-run-v1" not in html:
    fails.append("missing run save key")
if "function ordinal" not in html:
    fails.append("missing ordinal helper")
if 'id="btn-train"' not in html:
    fails.append("missing Train button")
if "Social Read" not in html:
    fails.append("missing Social Read")
if "not an EQ score" not in html:
    fails.append("missing Social Read honesty")
if html.count('id: "SR') < 40:
    fails.append("social pool too small")
if "SOCIAL_N = 10" not in html:
    fails.append("social run must be 10")
if "Frozen Nib" not in html or "Soft Win" not in html:
    fails.append("missing core Social Read stories")
if "Double Ask" not in html or "Guest Gift" not in html:
    fails.append("missing new Social Read stories")
if "T_ASSESS = 50" not in html:
    fails.append("reasoning timer must be 50s")
if "T_PRACTICE = 50" not in html:
    fails.append("reasoning practice timer must be 50s not 60")
if 'id="chip-time">1:00' in html:
    fails.append("HUD default still 1:00")
if 'textContent = "Social "' not in html and "Social \" +" not in html:
    fails.append("social chip should use short Social n/n")
if "#1a1028ee" in html:
    fails.append("span banner still washed overlay")
if "MEM_STUDY = 1.8" not in html or "MEM_PROBE = 12" not in html:
    fails.append("memory study/probe timers")
if 'id="mem-submit"' not in html or 'id="mem-shield"' not in html or 'id="mem-ready"' not in html:
    fails.append("memory study/ready/submit phases missing")
if "MEM_ARM_MS" not in html or "beginMemReady" not in html:
    fails.append("memory click-through arm missing")
if "SPD_LIMIT = 3.2" not in html:
    fails.append("speed timer must be 3.2s")
if re.search(r"\bvar SPD_LIMIT\s*=\s*(3\.84|4(\.0)?)\b", html):
    fails.append("SPD_LIMIT still 3.84 or 4")
if re.search(r"limit:\s*3\.84", html):
    fails.append("hardcoded 3.84 speed practice limit")
if "run.limit = SPD_LIMIT" not in html:
    fails.append("presentSpeed must pin SPD_LIMIT")
if "TEACH_DWELL = 2500" not in html:
    fails.append("missing teach dwell")
if 'id="btn-trivia"' in html:
    fails.append("splash Trivia button should be gone")
if "Quantum" not in html or "Camp life" not in html:
    fails.append("missing trivia categories")
if 'id="trivia-next"' not in html or 'id="span-banner"' not in html:
    fails.append("missing trivia next or span banner")
if "Warm Word" not in html:
    fails.append("missing Warm Word")
if "TRAIN_KEY" not in html:
    fails.append("missing train save key")
if "PRACTICE ONLY" not in html:
    fails.append("missing practice-only chip")
if 'id="btn-leave"' not in html:
    fails.append("missing Leave control")
if "leave-assess" not in html:
    fails.append("missing Leave Assess confirm")
if html.count('TQ') < 80:
    fails.append("trivia pool too small")
if re.search(r"connect wallet|wallet connect", html, re.I):
    fails.append("wallet connect string")

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("CHECK_OK")
