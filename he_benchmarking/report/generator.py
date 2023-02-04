import numpy as np
from collections import defaultdict


class ReportGenerator:
    def __init__(self, benchmarking_result: dict):
        self.benchmarking_result = benchmarking_result

    def generate(self):
        result = defaultdict(dict)
        for framework, ops in self.benchmarking_result.items():
            result[framework] = defaultdict(dict)
            for op, times in ops.items():
                times = np.array(times) * (10 ** 6)
                result[framework][op] = f"{np.mean(times):.2f}+-{np.std(times):.0f} ms"
        return result
