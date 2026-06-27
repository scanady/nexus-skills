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
