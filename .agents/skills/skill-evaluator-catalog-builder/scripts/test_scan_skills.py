import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scan_skills


def test_negated_credential_phrase_is_not_flagged(tmp_path):
    skill_dir = tmp_path
    skill_text = """
    ## Constraints
    - Hardcode API keys or secrets in any generated file
    - Do not store credentials in plain text
    """
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_text, encoding="utf-8")

    indicators = scan_skills.detect_external_indicators(skill_dir, skill_text)

    assert indicators["credential_refs"] is False


def test_explicit_credential_usage_is_flagged(tmp_path):
    skill_dir = tmp_path
    skill_text = """
    Use this API key to authenticate to the service and store the secret in a config file.
    """

    indicators = scan_skills.detect_external_indicators(skill_dir, skill_text)

    assert indicators["credential_refs"] is True


def test_script_regex_definitions_do_not_self_flag(tmp_path):
    skill_dir = tmp_path
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "scan_skills.py").write_text(
        '''import re

NETWORK_CALL_RE = re.compile(
    r"(requests\\.(get|post)|urllib|httpx|curl\\s)",
    re.IGNORECASE,
)
EXEC_RE = re.compile(r"(os\\.system|exec\\(|eval\\()", re.IGNORECASE)
CREDENTIAL_RE = re.compile(r"(API[_-]?KEY|SECRET|\\.env\\b)", re.IGNORECASE)
''',
        encoding="utf-8",
    )

    indicators = scan_skills.detect_external_indicators(skill_dir, "Plain local skill")

    assert indicators["credential_refs"] is False
    assert indicators["network_calls"] is False
    assert indicators["exec_patterns"] is False


def test_test_scripts_are_ignored_for_external_indicators(tmp_path):
    skill_dir = tmp_path
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "test_scan_skills.py").write_text(
        '''API_KEY = "demo"
requests.post("https://example.com")
os.system("echo hi")
''',
        encoding="utf-8",
    )

    indicators = scan_skills.detect_external_indicators(skill_dir, "Plain local skill")

    assert indicators["credential_refs"] is False
    assert indicators["network_calls"] is False
    assert indicators["exec_patterns"] is False


def test_runtime_script_indicators_are_still_flagged(tmp_path):
    skill_dir = tmp_path
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "run_scan.py").write_text(
        '''import requests
import os

API_KEY = "demo"
requests.post("https://example.com")
os.system("echo hi")
''',
        encoding="utf-8",
    )

    indicators = scan_skills.detect_external_indicators(skill_dir, "Plain local skill")

    assert indicators["credential_refs"] is True
    assert indicators["network_calls"] is True
    assert indicators["exec_patterns"] is True
