import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bidroom.scaffold import check_project, init_project  # noqa: E402


class ScaffoldTests(unittest.TestCase):
    def test_northstar_project_checks(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(check_project(root / "examples" / "northstar"), [])

    def test_init_creates_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pursuit"
            init_project(target, name="Acme Pursuit", owner="Jordan Lee")
            self.assertTrue((target / "manifest.json").exists())
            self.assertTrue((target / "policy.json").exists())
            self.assertTrue((target / "rooms" / "intake.md").exists())
            self.assertTrue((target / "agents" / "analyst.md").exists())
            self.assertEqual(check_project(target), [])


if __name__ == "__main__":
    unittest.main()
