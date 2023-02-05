import numpy as np
from collections import defaultdict


class ReportGenerator:
    """
    Class for processing benchmarking results
    to human-readable format
    """
    def __init__(self, benchmarking_result: dict):
        self.benchmarking_result = benchmarking_result

    def generate(self):
        """
        Compute mean, std in ms for every framework, operation combination
        Returns:

        """
        result = defaultdict(dict)
        for framework, ops in self.benchmarking_result.items():
            result[framework] = defaultdict(dict)
            for op, times in ops.items():
                times = np.array(times) * (10 ** 3)
                result[framework][op] = f"{np.mean(times):.2f}+-{np.std(times):.0f} ms"
        return result
