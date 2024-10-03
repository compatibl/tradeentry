# CompatibL Convince Package (Community Edition)
![GitHub](https://img.shields.io/github/license/compatibl/convince)
![PyPI - Downloads](https://img.shields.io/pypi/dm/convince)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/convince)
![PyPI](https://img.shields.io/pypi/v/convince)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/compatibl/convince/pulls)
## Summary

Better instruction following for large language models

Experiment results and completions can be examined at:

`tests/cl/convince/experiments`

To run the experiments, follow these steps:

### Setting up LLM keys and models

1. Copy the file called `sample_secrets.yaml` in project root to `.secrets.yaml` (note the dot in front)
   and replace placeholders for each LLM key with your own key, which can be obtained from the LLM providers.
   Alternatively, they can be set up using .env or envvars (running without the key will print instructions)
2. Edit the list of models in stub_llms.py if you prefer to run with a different set

### Running the experiments

1. IMPORTANT: Delete files `*.completions.*` and `*.expected.*` stored in subdirectories
   of the test location before running the tests
2. Run tests in `tests/cl/convince/experiments` under pytest to generate new results.

### Examining the results

1. The tests will generate new completions and expected test results using your LLM keys and you
   will be able to examine them using git diff.
2. Both completions and expected results will change compared to the saved results due to inherent
   variability of LLM response, however their statistics should remain the same


## Copyright

Each individual contributor holds copyright over their contributions to the
project. The project versioning is the sole means of recording all such
contributions and copyright details. Specifying corporate affiliation or
work email along with the commit shall have no bearing on copyright ownership
and does not constitute copyright assignment to the employer. Submitting a
contribution to this project constitutes your acceptance of these terms.

Because individual contributions are often changes to the existing code,
copyright notices in project files must specify The Project Contributors and
never an individual copyright holder.

