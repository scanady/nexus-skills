#!/usr/bin/env python3
"""
scan.py - Deterministic scanner for mechanical AI-writing and unidiomatic-copy tells.

This is a FLAGGER, not an autofixer and not a verdict. It catches the objective,
pattern-matchable tells (em dashes, curly quotes, emojis, knowledge-cutoff
disclaimers, chatbot artifacts, AI-vocabulary clusters, transition-word openers,
negative parallelism, inline-header lists, title-case headings, filler phrases,
significance inflation, hedging stacks, and likely strategy-copy abstractions).

Judgment-heavy patterns (faux-profound abstraction, unidiomatic collocation,
voice and register fit) are NOT scored here. The reviewer/editor applies the
core diagnostic question to every flag: "would a real person in this context
actually say it this way?" Flags are leads, not convictions.

Usage:
    python scan.py FILE [--json] [--summary] [--min-severity LOW|MED|HIGH]
    cat FILE | python scan.py - [--json]

Severity:
    HIGH  dead giveaway, almost always a tell
    MED   structural tell, usually worth fixing
    LOW   style/polish or low-confidence, check in context

Exit code is always 0 unless --strict is passed, in which case any HIGH finding
returns 2 (useful in CI / pre-commit). No third-party dependencies.
"""

import argparse
import json
import re
import sys

SEV_ORDER = {"LOW": 0, "MED": 1, "HIGH": 2}

# ---------------------------------------------------------------------------
# Pattern definitions.
# Each rule: (id, severity, compiled_regex, message, low_confidence_flag)
# low_confidence rules are real but prone to false positives; the message says so.
# ---------------------------------------------------------------------------

def _w(words):
    """Word-boundary, case-insensitive alternation for a list of words/phrases."""
    return re.compile(r"\b(" + "|".join(re.escape(x) for x in words) + r")\b", re.I)


RULES = []


def rule(rid, severity, pattern, message, flags=re.I, low_conf=False):
    RULES.append((rid, severity, re.compile(pattern, flags), message, low_conf))


# --- Style artifacts (mostly mechanical, high confidence) -------------------
rule("emdash", "HIGH", r"\u2014", "Em dash. Replace with comma, colon, period, or parentheses.", flags=0)
rule("endash", "MED", r"(?<=\w)\u2013(?=\w)", "En dash between words. Use a hyphen or reword.", flags=0)
rule("curly_quote", "LOW", r"[\u201c\u201d\u2018\u2019]", "Curly quote. Use a straight quote.", flags=0)
rule("emoji", "HIGH",
     r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F0FF\u2190-\u21FF\u2B00-\u2BFF\uFE0F]",
     "Emoji or decorative symbol. Remove from prose and headings.", flags=0)

# --- Chatbot / conversation artifacts (HIGH) --------------------------------
rule("chatbot_artifact", "HIGH",
     r"(i hope this helps|hope this helps|let me know if|would you like me to|"
     r"feel free to (ask|reach out)|here(?:'s| is) (?:a|an|the) (?:overview|summary|breakdown|rundown)|"
     r"as an ai language model|i(?:'m| am) (?:just )?an ai)",
     "Chatbot correspondence artifact pasted into content.")
rule("sycophancy", "HIGH",
     r"(great question|excellent question|excellent point|that(?:'s| is) (?:a )?(?:great|excellent|fantastic|wonderful) (?:question|point|idea)|"
     r"you(?:'re| are) absolutely right|good question|happy to help|certainly!|of course!|absolutely!)",
     "Sycophantic / servile opener. Cut and state the substance.")

# --- Knowledge-cutoff disclaimers (HIGH) ------------------------------------
rule("cutoff", "HIGH",
     r"(as of my last (?:training )?(?:update|knowledge)|up to my last (?:training )?update|"
     r"my (?:knowledge|training) (?:cut\s?off|cutoff)|based on (?:the )?available information|"
     r"while specific details (?:are|remain) (?:limited|scarce|not (?:extensively |widely )?(?:available|documented)))",
     "Knowledge-cutoff / availability disclaimer. State the fact or cut.")

# --- AI vocabulary cluster (MED, density-aware) -----------------------------
AI_VOCAB = [
    "delve", "tapestry", "testament", "underscore", "underscores", "underscoring",
    "pivotal", "showcase", "showcases", "showcasing", "intricate", "intricacies",
    "multifaceted", "realm", "foster", "fostering", "garner", "garnered",
    "leverage", "leveraging", "seamless", "seamlessly", "robust", "vibrant",
    "crucial", "vital", "elevate", "elevating", "unlock", "unlocking",
    "harness", "harnessing", "embark", "bustling", "nestled", "boasts",
    "navigate", "navigating", "landscape", "ever-evolving", "myriad",
    "plethora", "treasure trove", "in the realm of", "rich tapestry",
    "stands as", "serves as", "seamless integration", "cutting-edge",
    "game-changer", "game changer", "paradigm shift",
]
rule("ai_vocab", "MED", r"\b(" + "|".join(re.escape(w) for w in AI_VOCAB) + r")\b",
     "High-frequency AI-vocabulary word. Prefer a plainer choice.")

# --- Significance inflation (MED/HIGH) --------------------------------------
rule("significance", "MED",
     r"(stands as a testament|serves as a testament|marks? a (?:pivotal|key|crucial|defining) "
     r"(?:moment|point)|plays? a (?:crucial|vital|pivotal|key|significant) role|"
     r"underscor\w+ the (?:importance|significance)|highlight\w* the (?:importance|significance)|"
     r"in (?:today's|the) (?:rapidly )?(?:ever-)?(?:evolving|changing) (?:landscape|world|environment)|"
     r"rich (?:cultural )?(?:heritage|history|tapestry)|in the heart of|nestled (?:in|within|among))",
     "Significance / promotional inflation. Replace with a concrete fact.")

# --- Transition-word openers (MED) ------------------------------------------
rule("transition_opener", "MED",
     r"(?m)^[\s>*\-]*\b(furthermore|moreover|consequently|additionally|in addition|"
     r"similarly|likewise|nevertheless|notably|importantly|ultimately|"
     r"in conclusion|that said|with that said)\b",
     "Formal transition opening a line/paragraph. Vary or cut.", flags=re.I)

# --- Negative parallelism (MED) ---------------------------------------------
rule("neg_parallel", "MED",
     r"(it(?:'s| is) not (?:just|merely|only) about .{1,60}?,? it(?:'s| is)|"
     r"not (?:just|only|merely) .{1,40}? but (?:also )?|"
     r"isn(?:'t| not) (?:just|merely|only) .{1,40}? it(?:'s| is))",
     "Negative parallelism ('not just X, it's Y'). Usually filler; state Y directly.")

# --- Rule of three (LOW, low confidence) ------------------------------------
rule("rule_of_three", "LOW",
     r"\b(\w+ing|\w{3,}),\s+(\w+ing|\w{3,}),\s+and\s+(\w+ing|\w{3,})\b",
     "Possible forced rule-of-three triple. Check it is not padding.", low_conf=True)

# --- Inline-header vertical list (MED) --------------------------------------
rule("inline_header_list", "MED",
     r"(?m)^[\s>]*[-*+]\s*\*\*[^*]+\*\*\s*:",
     "Bolded inline-header list item. Convert to flowing prose if possible.", flags=re.I)

# --- Title Case heading (LOW) -----------------------------------------------
rule("title_case_heading", "LOW",
     r"(?m)^#{1,6}\s+([A-Z][a-z]+\s+){2,}[A-Z][a-z]+\s*$",
     "Title Case heading. Use sentence case unless house style requires otherwise.",
     flags=0, low_conf=True)

# --- Filler phrases (MED) ---------------------------------------------------
rule("filler", "MED",
     r"(in order to|due to the fact that|at this point in time|in the event that|"
     r"has the ability to|have the ability to|it is important to note that|"
     r"it should be noted that|when it comes to|for the purpose of|"
     r"in spite of the fact that|with regard to the fact that)",
     "Filler phrase. Compress.")

# --- Hedging stacks (LOW) ---------------------------------------------------
rule("hedge_stack", "LOW",
     r"(could potentially|might possibly|may possibly|it could be argued that|"
     r"it might be argued that|possibly might|potentially could|"
     r"some(?:what)? (?:kind|sort) of)",
     "Stacked hedging. Keep at most one qualifier.")

# --- Strategy / faux-profound copy (MED, low confidence, needs human check) -
rule("strategy_abstraction", "MED",
     r"(move with intention|unlock(?:ing)? clarity|hold the tension|sit with the (?:complexity|discomfort)|"
     r"name the (?:bet|tension|pressure|real (?:question|pressure))|create space for|"
     r"lean into|the path forward|true north|meaningful (?:change|impact|outcomes)|"
     r"drive(?:s)? (?:meaningful )?(?:outcomes|impact|growth)|with intentionality|"
     r"at the deepest level|the thing under the thing)",
     "Faux-profound / abstract strategy phrasing. Confirm, then rewrite to a concrete action, stake, or proof.",
     low_conf=True)

# --- Participial '-ing' tail (LOW, low confidence) --------------------------
rule("ing_tail", "LOW",
     r",\s+(highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|"
     r"contributing|showcasing|fostering|cultivating|encompassing|demonstrating|"
     r"signaling|representing)\b",
     "Trailing '-ing' participial phrase. Often tacks on fake depth; verify it adds information.",
     low_conf=True)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def line_col(text, idx):
    """Return (line_no, col_no) 1-indexed for a character offset."""
    before = text[:idx]
    line = before.count("\n") + 1
    col = idx - (before.rfind("\n"))
    return line, col


def scan(text):
    findings = []
    for rid, severity, rx, msg, low_conf in RULES:
        for m in rx.finditer(text):
            line, col = line_col(text, m.start())
            snippet = m.group(0).replace("\n", " ").strip()
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            findings.append({
                "id": rid,
                "severity": severity,
                "line": line,
                "col": col,
                "match": snippet,
                "message": msg,
                "low_confidence": low_conf,
            })
    findings.sort(key=lambda f: (-SEV_ORDER[f["severity"]], f["line"], f["col"]))
    return findings


def density_metrics(text):
    words = re.findall(r"\b\w+\b", text)
    n_words = max(len(words), 1)
    bold = len(re.findall(r"\*\*[^*\n]+\*\*", text))
    ai_hits = sum(1 for _ in re.finditer(
        r"\b(" + "|".join(re.escape(w) for w in AI_VOCAB) + r")\b", text, re.I))
    return {
        "words": n_words,
        "bold_runs": bold,
        "bold_per_100w": round(bold / n_words * 100, 2),
        "ai_vocab_hits": ai_hits,
        "ai_vocab_per_100w": round(ai_hits / n_words * 100, 2),
    }


def human_report(findings, metrics, min_sev):
    out = []
    shown = [f for f in findings if SEV_ORDER[f["severity"]] >= SEV_ORDER[min_sev]]
    counts = {"HIGH": 0, "MED": 0, "LOW": 0}
    for f in findings:
        counts[f["severity"]] += 1

    out.append("SCAN SUMMARY")
    out.append(f"  HIGH {counts['HIGH']}   MED {counts['MED']}   LOW {counts['LOW']}"
               f"   (showing >= {min_sev})")
    out.append(f"  words {metrics['words']}   "
               f"bold/100w {metrics['bold_per_100w']}   "
               f"AI-vocab/100w {metrics['ai_vocab_per_100w']}")
    if metrics["bold_per_100w"] > 2:
        out.append("  ! boldface density is high (>2 per 100 words)")
    if metrics["ai_vocab_per_100w"] > 1.5:
        out.append("  ! AI-vocabulary density is high (>1.5 per 100 words)")
    out.append("")

    if not shown:
        out.append("No findings at or above the chosen severity.")
        return "\n".join(out)

    out.append("FINDINGS (line:col  severity  id)")
    for f in shown:
        tag = " [low-confidence]" if f["low_confidence"] else ""
        out.append(f"  {f['line']}:{f['col']}  {f['severity']:<4} {f['id']}{tag}")
        out.append(f"      match: {f['match']!r}")
        out.append(f"      {f['message']}")
    out.append("")
    out.append("Flags are leads, not verdicts. Apply the core test to each: "
               "would a real person in this context say it this way?")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description="Scan copy for mechanical AI-writing tells.")
    p.add_argument("file", help="Path to a text/markdown file, or - for stdin.")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of a human report.")
    p.add_argument("--summary", action="store_true", help="Print only the summary counts.")
    p.add_argument("--min-severity", default="LOW", choices=["LOW", "MED", "HIGH"],
                   help="Hide findings below this severity in the human report.")
    p.add_argument("--strict", action="store_true",
                   help="Exit code 2 if any HIGH finding is present.")
    args = p.parse_args(argv)

    if args.file == "-":
        text = sys.stdin.read()
    else:
        with open(args.file, "r", encoding="utf-8") as fh:
            text = fh.read()

    findings = scan(text)
    metrics = density_metrics(text)

    if args.json:
        print(json.dumps({"findings": findings, "metrics": metrics}, indent=2))
    elif args.summary:
        counts = {"HIGH": 0, "MED": 0, "LOW": 0}
        for f in findings:
            counts[f["severity"]] += 1
        print(f"HIGH {counts['HIGH']}  MED {counts['MED']}  LOW {counts['LOW']}")
    else:
        print(human_report(findings, metrics, args.min_severity))

    if args.strict and any(f["severity"] == "HIGH" for f in findings):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
