import unittest

from VALIDATION_SUITE.run_tests import make_json_safe, resolve_test_vectors_base


class ValidationSuiteHelpersTest(unittest.TestCase):
    def test_make_json_safe_converts_nested_bytes(self):
        value = {
            "outer": [
                {"payload": b"\x00\x01"},
                {"inner": [b"\x02"]},
            ]
        }

        self.assertEqual(
            make_json_safe(value),
            {
                "outer": [
                    {"payload": "0001"},
                    {"inner": ["02"]},
                ]
            },
        )

    def test_resolve_test_vectors_base_matches_available_layout(self):
        base = resolve_test_vectors_base()

        self.assertTrue((base / "metadata.json").exists())
        self.assertTrue((base / "inputs").is_dir())


if __name__ == "__main__":
    unittest.main()
