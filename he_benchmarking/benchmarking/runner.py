import time
from collections import defaultdict
import inspect
from .operations import DefaultOperations, PlainTextOperations
from data.generator import DataGenerator, get_operation_names


class Benchmark:
    def __init__(self, encryption_classes, num_runs=10):
        self.encryption_classes = encryption_classes
        self.num_runs = num_runs

    def run(self):
        """
        Measure time for operations in every iteration for every operation
        :return:
        """
        data_gen = DataGenerator()
        result = defaultdict(dict)
        plain_text_operations = list(get_operation_names(PlainTextOperations))
        for enc in self.encryption_classes:
            class_object = enc()
            impl_name = str(enc.__name__)
            result[impl_name] = defaultdict(list)
            for operation in get_operation_names(DefaultOperations):
                # 1. Do preparations
                operation_data = getattr(data_gen, operation, None)
                operation_function = getattr(class_object, operation, None)
                if not operation_function:
                    continue
                if not operation_data:
                    continue
                inputs, ground_truth = operation_data()
                if "int" in operation:
                    encryption_func = getattr(class_object, "encryption_int_from_encoding")
                elif "float" in operation:
                    encryption_func = getattr(class_object, "encryption_float_from_encoding")
                else:
                    raise ValueError("Only encryption for int or float are supported")

                if not isinstance(inputs, tuple):
                    inputs = (inputs,)
                if operation not in plain_text_operations:
                    inputs = list(map(encryption_func, inputs))
                # 2. Run and measure time
                for i_run in range(self.num_runs):
                    start = time.time()
                    operation_function(*inputs)
                    end = time.time()
                    result[impl_name][operation].append(end - start)
                # 3. Save result
        return result
