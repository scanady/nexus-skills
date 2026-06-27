#!/usr/bin/env python3
"""Regression tests for assemble_catalog.py weighted usage scoring."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("assemble_catalog.py")


class AssembleCatalogWeightedUsageTests(unittest.TestCase):
    def test_usage_weighted_fields_and_domain_floor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            scan_path = tmp / "scan.json"
            eval_path = tmp / "eval.json"
            out_path = tmp / "out.json"

            scan_data = {
                "source_directory": str(tmp),
                "total_skills": 1,
                "skills": [
                    {
                        "path": "content-behavioral-nudge-unit/SKILL.md",
                        "name": "content-behavioral-nudge-unit",
                        "frontmatter": {
                            "name": "content-behavioral-nudge-unit",
                            "description": "Use when asked to nudge behavior with behavioral science methods.",
                        },
                        "structure": {
                            "has_scripts": False,
                            "has_references": True,
                            "has_agents": False,
                            "has_assets": False,
                            "has_license_file": False,
                            "file_count": 4,
                            "estimated_tokens": 640,
                        },
                        "script_languages": ["none"],
                        "license": "unspecified",
                        "body_excerpt": "Phase 1 - Diagnose. Phase 2 - Generate. Apply nudge theory and choice architecture.",
                    }
                ],
            }

            eval_data = [
                {
                    "name": "content-behavioral-nudge-unit",
                    "evaluation": {
                        "usage_value": {
                            "score": 2,
                            "rationale": "Domain-specific skill with clear purpose.",
                            "sub_scores": {
                                "problem_clarity": 5,
                                "audience_breadth": 4,
                                "capability_gap": 4,
                                "actionability": 4,
                                "reusability": 4,
                            },
                            "domain_calibration_bonus": 0.3,
                        },
                        "security_risk": {
                            "rating": "low",
                            "rationale": "Low risk",
                            "findings": [],
                            "sub_scores": {
                                "data_privacy": 5,
                                "prompt_injection": 5,
                                "illegal_content": 5,
                                "bias": 5,
                                "system_integrity": 5,
                                "untrusted_communication": 5,
                            },
                        },
                        "executability": {
                            "score": 4,
                            "completeness": 4,
                            "determinism": 4,
                            "consistency": 4,
                            "usability": 4,
                            "rationale": "Good",
                        },
                        "invocability": {"score": 3, "rationale": "Adequate"},
                        "over_specification_risk": {
                            "flagged": False,
                            "rationale": "Generalizable",
                        },
                        "core_capabilities": "Applies nudge theory.",
                        "external_requirements_indicator": "self-contained",
                        "external_requirements": ["none"],
                        "script_languages": ["none"],
                        "license": "unspecified",
                    },
                }
            ]

            scan_path.write_text(json.dumps(scan_data, indent=2), encoding="utf-8")
            eval_path.write_text(json.dumps(eval_data, indent=2), encoding="utf-8")

            subprocess.run(
                [
                    "python",
                    str(SCRIPT_PATH),
                    str(scan_path),
                    str(eval_path),
                    "--output",
                    str(out_path),
                ],
                check=True,
            )

            out = json.loads(out_path.read_text(encoding="utf-8"))
            usage = out["skills"][0]["evaluation"]["usage_value"]

            self.assertEqual(usage["method_version"], "weighted-v2")
            self.assertAlmostEqual(usage["weighted_score"], 4.25, places=2)
            self.assertAlmostEqual(usage["domain_calibration_bonus"], 0.3, places=2)
            self.assertEqual(usage["sub_scores"]["problem_clarity"], 5)
            # Rationale mentions domain-specific; score must be >= 3 by guard.
            self.assertGreaterEqual(usage["score"], 3)

    def test_fails_when_evaluation_is_missing_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            scan_path = tmp / "scan.json"
            eval_path = tmp / "eval.json"
            out_path = tmp / "out.json"

            scan_data = {
                "source_directory": str(tmp),
                "total_skills": 1,
                "skills": [
                    {
                        "path": "one/SKILL.md",
                        "name": "one",
                        "frontmatter": {"name": "one", "description": "Use when..."},
                        "structure": {
                            "has_scripts": False,
                            "has_references": False,
                            "has_agents": False,
                            "has_assets": False,
                            "has_license_file": False,
                            "file_count": 1,
                            "estimated_tokens": 100,
                        },
                        "script_languages": ["none"],
                        "license": "unspecified",
                        "body_excerpt": "",
                    }
                ],
            }

            scan_path.write_text(json.dumps(scan_data, indent=2), encoding="utf-8")
            eval_path.write_text("[]", encoding="utf-8")

            proc = subprocess.run(
                [
                    "python",
                    str(SCRIPT_PATH),
                    str(scan_path),
                    str(eval_path),
                    "--output",
                    str(out_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(proc.returncode, 2)
            self.assertIn("missing evaluations", proc.stderr.lower())

    def test_dedupes_duplicate_names_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            scan_path = tmp / "scan.json"
            eval_path = tmp / "eval.json"
            out_path = tmp / "out.json"

            scan_data = {
                "source_directory": str(tmp),
                "total_skills": 2,
                "skills": [
                    {
                        "path": "a/SKILL.md",
                        "name": "dup-skill",
                        "frontmatter": {"name": "dup-skill", "description": "Use when..."},
                        "structure": {
                            "has_scripts": False,
                            "has_references": False,
                            "has_agents": False,
                            "has_assets": False,
                            "has_license_file": False,
                            "file_count": 1,
                            "estimated_tokens": 100,
                        },
                        "script_languages": ["none"],
                        "license": "unspecified",
                        "body_excerpt": "",
                    },
                    {
                        "path": "b/SKILL.md",
                        "name": "dup-skill",
                        "frontmatter": {"name": "dup-skill", "description": "Use when..."},
                        "structure": {
                            "has_scripts": False,
                            "has_references": False,
                            "has_agents": False,
                            "has_assets": False,
                            "has_license_file": False,
                            "file_count": 1,
                            "estimated_tokens": 100,
                        },
                        "script_languages": ["none"],
                        "license": "unspecified",
                        "body_excerpt": "",
                    },
                ],
            }

            eval_data = [
                {
                    "name": "dup-skill",
                    "evaluation": {
                        "usage_value": {
                            "score": 4,
                            "rationale": "Domain-specific skill with clear purpose.",
                            "sub_scores": {
                                "problem_clarity": 4,
                                "audience_breadth": 4,
                                "capability_gap": 4,
                                "actionability": 4,
                                "reusability": 4,
                            },
                            "domain_calibration_bonus": 0.0,
                        },
                        "security_risk": {
                            "rating": "low",
                            "rationale": "Low risk",
                            "findings": [],
                            "sub_scores": {
                                "data_privacy": 5,
                                "prompt_injection": 5,
                                "illegal_content": 5,
                                "bias": 5,
                                "system_integrity": 5,
                                "untrusted_communication": 5,
                            },
                        },
                        "executability": {
                            "score": 4,
                            "completeness": 4,
                            "determinism": 4,
                            "consistency": 4,
                            "usability": 4,
                            "rationale": "Good",
                        },
                        "invocability": {"score": 4, "rationale": "Good"},
                        "over_specification_risk": {
                            "flagged": False,
                            "rationale": "Generalizable",
                        },
                        "core_capabilities": "Does a thing.",
                        "external_requirements_indicator": "self-contained",
                        "external_requirements": ["none"],
                        "script_languages": ["none"],
                        "license": "unspecified",
                    },
                }
            ]

            scan_path.write_text(json.dumps(scan_data, indent=2), encoding="utf-8")
            eval_path.write_text(json.dumps(eval_data, indent=2), encoding="utf-8")

            subprocess.run(
                [
                    "python",
                    str(SCRIPT_PATH),
                    str(scan_path),
                    str(eval_path),
                    "--output",
                    str(out_path),
                ],
                check=True,
            )

            out = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(len(out.get("skills", [])), 1)

    def test_resolves_evaluation_by_path_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            scan_path = tmp / "scan.json"
            eval_path = tmp / "eval.json"
            out_path = tmp / "out.json"

            scan_data = {
                "source_directory": str(tmp),
                "total_skills": 1,
                "skills": [
                    {
                        "path": "strategy-decision/SKILL.md",
                        "name": "thinking-get-unstuck",
                        "frontmatter": {
                            "name": "thinking-get-unstuck",
                            "description": "Use when stuck.",
                        },
                        "structure": {
                            "has_scripts": False,
                            "has_references": False,
                            "has_agents": False,
                            "has_assets": False,
                            "has_license_file": False,
                            "file_count": 1,
                            "estimated_tokens": 100,
                        },
                        "script_languages": ["none"],
                        "license": "unspecified",
                        "body_excerpt": "",
                    }
                ],
            }

            eval_data = [
                {
                    "name": "strategy-decision",
                    "evaluation": {
                        "usage_value": {
                            "score": 4,
                            "rationale": "Domain-specific skill with clear purpose.",
                            "sub_scores": {
                                "problem_clarity": 4,
                                "audience_breadth": 4,
                                "capability_gap": 4,
                                "actionability": 4,
                                "reusability": 4,
                            },
                            "domain_calibration_bonus": 0.3,
                        },
                        "security_risk": {
                            "rating": "low",
                            "rationale": "Low risk",
                            "findings": [],
                            "sub_scores": {
                                "data_privacy": 5,
                                "prompt_injection": 5,
                                "illegal_content": 5,
                                "bias": 5,
                                "system_integrity": 5,
                                "untrusted_communication": 5,
                            },
                        },
                        "executability": {
                            "score": 4,
                            "completeness": 4,
                            "determinism": 4,
                            "consistency": 4,
                            "usability": 4,
                            "rationale": "Good",
                        },
                        "invocability": {"score": 4, "rationale": "Good"},
                        "over_specification_risk": {
                            "flagged": False,
                            "rationale": "Generalizable",
                        },
                        "core_capabilities": "Does a thing.",
                        "external_requirements_indicator": "self-contained",
                        "external_requirements": ["none"],
                        "script_languages": ["none"],
                        "license": "unspecified",
                    },
                }
            ]

            scan_path.write_text(json.dumps(scan_data, indent=2), encoding="utf-8")
            eval_path.write_text(json.dumps(eval_data, indent=2), encoding="utf-8")

            subprocess.run(
                [
                    "python",
                    str(SCRIPT_PATH),
                    str(scan_path),
                    str(eval_path),
                    "--output",
                    str(out_path),
                ],
                check=True,
            )

            out = json.loads(out_path.read_text(encoding="utf-8"))
            skill = out["skills"][0]
            usage = skill["evaluation"]["usage_value"]
            self.assertEqual(usage.get("method_version"), "weighted-v2")
            self.assertGreaterEqual(usage.get("score", 0), 3)

    def test_rewrites_not_evaluated_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            scan_path = tmp / "scan.json"
            eval_path = tmp / "eval.json"
            out_path = tmp / "out.json"

            scan_data = {
                "source_directory": str(tmp),
                "total_skills": 1,
                "skills": [
                    {
                        "path": "sample/SKILL.md",
                        "name": "sample",
                        "frontmatter": {"name": "sample", "description": "Use when..."},
                        "structure": {
                            "has_scripts": False,
                            "has_references": False,
                            "has_agents": False,
                            "has_assets": False,
                            "has_license_file": False,
                            "file_count": 1,
                            "estimated_tokens": 100,
                        },
                        "script_languages": ["none"],
                        "license": "unspecified",
                        "body_excerpt": "",
                    }
                ],
            }

            eval_data = [
                {
                    "name": "sample",
                    "evaluation": {
                        "usage_value": {
                            "score": 0,
                            "rationale": "Not evaluated",
                            "sub_scores": {
                                "problem_clarity": 0,
                                "audience_breadth": 0,
                                "capability_gap": 0,
                                "actionability": 0,
                                "reusability": 0,
                            },
                            "domain_calibration_bonus": 0,
                        },
                        "security_risk": {
                            "rating": "unknown",
                            "rationale": "Not evaluated",
                            "findings": [],
                            "sub_scores": {
                                "data_privacy": 0,
                                "prompt_injection": 0,
                                "illegal_content": 0,
                                "bias": 0,
                                "system_integrity": 0,
                                "untrusted_communication": 0,
                            },
                        },
                        "executability": {
                            "score": 0,
                            "completeness": 0,
                            "determinism": 0,
                            "consistency": 0,
                            "usability": 0,
                            "rationale": "Not evaluated",
                        },
                        "invocability": {"score": 0, "rationale": "Not evaluated"},
                        "over_specification_risk": {
                            "flagged": False,
                            "rationale": "Not evaluated",
                        },
                        "core_capabilities": "Not evaluated",
                        "external_requirements_indicator": "unknown",
                        "external_requirements": ["unknown"],
                        "script_languages": ["none"],
                        "license": "unspecified",
                    },
                }
            ]

            scan_path.write_text(json.dumps(scan_data, indent=2), encoding="utf-8")
            eval_path.write_text(json.dumps(eval_data, indent=2), encoding="utf-8")

            subprocess.run(
                [
                    "python",
                    str(SCRIPT_PATH),
                    str(scan_path),
                    str(eval_path),
                    "--output",
                    str(out_path),
                ],
                check=True,
            )

            out = json.loads(out_path.read_text(encoding="utf-8"))
            evaluation_blob = json.dumps(out["skills"][0]["evaluation"]).lower()
            self.assertNotIn("not evaluated", evaluation_blob)


if __name__ == "__main__":
    unittest.main()