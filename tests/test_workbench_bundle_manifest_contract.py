"""Tests for the canonical lowercase workbench bundle-manifest folder contract."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl import (
    load_manage_architecture_source,
)


class WorkbenchBundleManifestContractTests(unittest.TestCase):
    """Verify generated bundle manifests can live under workbench/bundle_manifest."""

    def test_workbench_bundle_manifest_folder_is_accepted(self) -> None:
        source = load_manage_architecture_source()

        self.assertIn(
            'BUNDLE_SAFETY_WORKBENCH_MANIFEST_PREFIX = "workbench/bundle_manifest/"',
            source,
        )
        self.assertIn(
            'BUNDLE_SAFETY_MANIFEST_PREFIX = "_project_reference/BUNDLE_MANIFEST/"',
            source,
        )
        self.assertIn(
            'BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX = "workbench/_bundle_temp/"',
            source,
        )
        self.assertIn("BUNDLE_SAFETY_MANIFEST_PREFIXES", source)
        self.assertIn("workbench/bundle_manifest", source)
        self.assertNotIn(
            'BUNDLE_SAFETY_WORKBENCH_MANIFEST_PREFIX = "workbench/BUNDLE_MANIFEST/"',
            source,
        )

    def test_hidden_project_reference_is_not_the_canonical_manifest_folder(self) -> None:
        source = load_manage_architecture_source()

        self.assertNotIn(
            'BUNDLE_SAFETY_HIDDEN_REFERENCE_MANIFEST_PREFIX = ".project_reference/BUNDLE_MANIFEST/"',
            source,
        )


if __name__ == "__main__":
    unittest.main()
