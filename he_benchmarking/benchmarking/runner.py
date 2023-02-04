import time
from collections import defaultdict


class Benchmark:
    def __init__(self, encryption_classes, num_runs=10):
        self.encryption_classes = encryption_classes
        self.num_runs = num_runs

    def run(self):
        """
        Measure time for operations in every iteration for every operation
        :return:
        """
        result = defaultdict(dict)
        for enc in self.encryption_classes:
            class_object = enc()
            impl_name = enc.__name__
            result[impl_name] = defaultdict(list)
            for operation in class_object.operation_list:
                # 1. Do preparations
                operation_function = getattr(class_object, operation, None)
                if not operation_function:
                    continue
                # 2. Run and measure time
                for i_run in range(self.num_runs):
                    start = time.time()
                    operation_function()
                    end = time.time()
                    result[impl_name][operation].append(end - start)
                # 3. Save result
        return result
