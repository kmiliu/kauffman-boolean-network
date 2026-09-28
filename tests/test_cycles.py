"""Regression tests for attractor identity, independent of notebook execution order."""
import json
from pathlib import Path
import unittest

# Core regression checks use only the standard library; plotting is not exercised here.
scope = {}
notebook = json.loads((Path(__file__).resolve().parents[1] / "kauffman-boolean-network.ipynb").read_text())
for cell in notebook["cells"]:
    source = "".join(cell["source"])
    if cell["cell_type"] == "code" and "# PART 6:" not in source:
        exec(compile(source.replace("import matplotlib.pyplot as plt", ""), "notebook", "exec"), scope)

class CycleTests(unittest.TestCase):
    def test_repeated_endpoint_excluded(self):
        self.assertEqual(scope["extract_attractor"]([[0], [1], [0]], 2, 0), ([0], [1]))

    def test_rotation_identity(self):
        a = scope["extract_attractor"]([[0], [1], [0]], 2, 0)
        b = scope["extract_attractor"]([[1], [0], [1]], 2, 0)
        self.assertEqual(a, b)

    def test_fixed_point_and_two_cycle(self):
        network = scope["net"](1)
        network.nodes[0].type = 0
        self.assertEqual(scope["get_attractor_from_start"](network, [1]), ([0],))
        network.nodes[0].type = 2
        self.assertEqual(scope["get_attractor_from_start"](network, [0]), ([0], [1]))

    def test_generun_reports_exact_cycle_length(self):
        scope["random"].seed(42)
        for _ in range(20):
            (length, start), _, states = scope["generun2"](3)
            self.assertEqual(len(states) - 1 - start, length)
            self.assertEqual(states[start], states[-1])

    def test_summary_has_no_significance_claim(self):
        stats = scope["calculate_statistics"]([20, 40, 60])
        self.assertEqual(stats["mean"], 40)
        self.assertNotIn("significant", stats)
        with self.assertRaises(ValueError):
            scope["calculate_statistics"]([50])

if __name__ == "__main__":
    unittest.main()
