# Mutation Sensitivity in Random Boolean Networks

An exploratory simulation of how a single node's Boolean rule can change the long-run attractor of a synchronous Kauffman-style network.

## Experiment

Each network has two randomly sampled inputs per node (self-inputs and duplicate inputs are allowed). Each node receives one of the 16 two-input Boolean functions uniformly at random. Starting from a random binary state, all nodes update synchronously until a state repeats.

For each node, the experiment samples one replacement rule uniformly from the other 15 rules, restarts from the **same initial state**, and compares the resulting attractor with the baseline. Cycles are compared up to rotation. Sensitivity is the percentage of these sampled single-node mutations that change the attractor.

The default run uses seed **42**, **20 independently generated networks** at each size **N = 10, 15, 20**, and a separate **10-network** cascade exploration at **N = 15**. It does not enumerate all replacement rules or all initial states.

| Network size | Mean sensitivity | Approximate 95% normal interval |
| --- | --- | --- |
| 10 | 75.00% | 67.68–82.32% |
| 15 | 71.67% | 65.53–77.80% |
| 20 | 69.25% | 63.04–75.46% |

The table and [machine-readable results](outputs/results.json) are produced by the corrected notebook. Per-network rates are included for inspection. This is a finite simulation of the specified ensemble, not evidence about a particular biological regulatory network.

## Reproduce

Use Python 3.10 or newer in an isolated environment:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_analysis.py
```

`run_analysis.py` executes the notebook's code cells in order and writes `outputs/sensitivity.png` and `outputs/results.json`. For interactive exploration, open `kauffman-boolean-network.ipynb` in a notebook editor with the same environment and run all cells from a fresh kernel. The execution cell resets the seed; changing parameters or the random-call sequence changes the result. Exact versions used for validation are recorded in `outputs/environment.txt`.

## Interpreting the summaries

- **50% is an arbitrary visual reference**, not a theoretically justified random baseline or null hypothesis for attractor changes. No significance flag or hypothesis test is reported.
- Error bars use **mean ± 1.96 × sample SD / √number of networks**. These are approximate 95% normal intervals for the ensemble mean under independent network sampling and an adequate normal approximation; coverage is not guaranteed with 20 bounded, discrete rates. They are not exact Student-t intervals and are not clipped to 0–100%.
- Mutations within one network share its topology and initial state. The network, not the individual mutation, is the replication unit for these intervals. No test of differences between network sizes is performed.
- The “cascade” histogram includes only changed attractors with **equal cycle lengths**. It counts nodes differing at any position after independently choosing the lexicographically smallest rotation of each cycle. This is a phase-convention-dependent comparison, not a measured causal propagation process. Mutations that change cycle length are counted separately in the pie chart.
- Exhaustive trajectory search can require exponentially many states; the current implementation stores visited states and linearly searches them. Larger networks can be slow and memory-intensive.

## Correctness and provenance

The original notebook included the repeated terminal state in attractor comparisons and recomputed a cycle length after appending it. The updated code excludes that endpoint and retains the first detected cycle length. Regression tests cover fixed points, two-cycles, rotation invariance, and cycle-length bookkeeping.

Old cached output has been cleared because it used the earlier cycle handling and labeled a 50% comparison as significant. The committed table and JSON are newly generated simulation artifacts, not relabeled historical results. No external or private data is needed.

| File | Purpose |
| --- | --- |
| `kauffman-boolean-network.ipynb` | Model, mutation experiment, summaries, and visualization |
| `run_analysis.py` | Sequential execution without a notebook server |
| `tests/test_cycles.py` | Attractor and summary regression checks |
| `requirements.txt` | Runtime and notebook dependencies |
| `outputs/` | Trial rates and validation environment; figures are generated on execution |
