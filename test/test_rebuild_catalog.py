import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "catalog" / "rebuild-catalog.py"

spec = importlib.util.spec_from_file_location("rebuild_catalog", MODULE_PATH)
rebuild_catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rebuild_catalog)


def test_derive_core_capabilities_falls_back_to_frontmatter_description():
    frontmatter = {"description": "Ultra-compressed communication mode."}

    assert rebuild_catalog.derive_core_capabilities(frontmatter, ">-.") == frontmatter["description"]
    assert rebuild_catalog.derive_core_capabilities(frontmatter, ">.") == frontmatter["description"]
    assert rebuild_catalog.derive_core_capabilities(frontmatter, "Not evaluated") == frontmatter["description"]
    assert rebuild_catalog.derive_core_capabilities(frontmatter, "Real capability text") == "Real capability text"
