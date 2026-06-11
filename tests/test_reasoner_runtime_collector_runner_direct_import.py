"""Direct import protection for the canonical reasoner runtime collector runner."""

from __future__ import annotations

import unittest

import kanda_reasoner_app.reasoner_runtime_collector.runner as runtime_runner


class ReasonerRuntimeCollectorRunnerDirectImportTests(unittest.TestCase):
    """Protect the public import contract for the runtime collector runner."""

    def test_runtime_collector_runner_imports(self):
        """The canonical runtime collector runner must remain importable."""
        self.assertIsNotNone(runtime_runner)
        self.assertEqual(
            "kanda_reasoner_app.reasoner_runtime_collector.runner",
            runtime_runner.__name__,
        )


if __name__ == "__main__":
    unittest.main()
