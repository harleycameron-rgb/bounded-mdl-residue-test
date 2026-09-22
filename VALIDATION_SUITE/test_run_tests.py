import unittest
from pathlib import Path
from unittest.mock import patch

import REFERENCE_IMPLEMENTATION.core as impl
from VALIDATION_SUITE.run_tests import make_json_safe, resolve_test_vector_paths, run_compression_tests


class ValidationSuiteHelpersTest(unittest.TestCase):
    def test_make_json_safe_converts_nested_bytes(self):
        value = {
            "outer": [
                {"payload": b"\x00\x01"},
                {"inner": (b"\x02",)},
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

    def test_resolve_test_vector_paths_prefers_primary_layout(self):
        root = Path("/repo")
        base = root / "TEST_VECTORS"
        inputs_dir = base / "inputs"
        metadata_file = base / "metadata.json"

        with patch("VALIDATION_SUITE.run_tests.ROOT", root):
            with patch.object(Path, "is_dir", autospec=True, side_effect=lambda path: path == inputs_dir):
                with patch.object(Path, "exists", autospec=True, side_effect=lambda path: path == metadata_file):
                    resolved_inputs, resolved_metadata = resolve_test_vector_paths()

        self.assertEqual((resolved_inputs, resolved_metadata), (inputs_dir, metadata_file))

    def test_resolve_test_vector_paths_supports_nested_metadata_layout(self):
        root = Path("/repo")
        base = root / "TEST_VECTORS"
        inputs_dir = base / "inputs"
        metadata_file = base / "TEST_VECTORS" / "metadata.json"

        def exists(path):
            return path == metadata_file

        with patch("VALIDATION_SUITE.run_tests.ROOT", root):
            with patch.object(Path, "is_dir", autospec=True, side_effect=lambda path: path == inputs_dir):
                with patch.object(Path, "exists", autospec=True, side_effect=exists):
                    resolved_inputs, resolved_metadata = resolve_test_vector_paths()

        self.assertEqual((resolved_inputs, resolved_metadata), (inputs_dir, metadata_file))

    def test_resolve_test_vector_paths_raises_when_layout_missing(self):
        root = Path("/repo")

        with patch("VALIDATION_SUITE.run_tests.ROOT", root):
            with patch.object(Path, "is_dir", autospec=True, return_value=False):
                with patch.object(Path, "exists", autospec=True, return_value=False):
                    with self.assertRaises(FileNotFoundError):
                        resolve_test_vector_paths()

    def test_run_compression_tests_returns_json_friendly_summary(self):
        vectors = [{"id": "sample", "text": "abc", "category": "test", "meta": {}}]
        mock_core = {"signature": "sig", "compressed_bytes": b"abcd"}

        with patch("VALIDATION_SUITE.run_tests.load_test_vectors", return_value=vectors):
            with patch("VALIDATION_SUITE.run_tests.impl.compress_text", return_value=mock_core) as compress_text:
                results = run_compression_tests()

        compress_text.assert_called_once_with("abc")
        self.assertEqual(
            results,
            [{
                "id": "sample",
                "compressed_core": {
                    "signature": "sig",
                    "compressed_size": 4,
                },
            }],
        )

    def test_extract_residue_supports_legacy_and_current_signatures(self):
        core = impl.compress_text("abc")

        self.assertEqual(
            impl.extract_residue("abc"),
            impl.extract_residue("abc", core),
        )


if __name__ == "__main__":
    unittest.main()
