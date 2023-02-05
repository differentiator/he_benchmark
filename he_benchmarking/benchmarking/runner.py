import time
import inspect
from collections import defaultdict

from .operations import DefaultOperations, PlainTextOperations
from data.generator import DataGenerator, get_operation_names
from utils.logging import logger


class Benchmark:
    """
    The main class that gathers specified
    implementations of Fully Homomorphic Encryption and
    DataGenerator and prepares data and measures time
    """
    def __init__(self, encryption_classes, num_runs=10):
        self.encryption_classes = encryption_classes
        self.num_runs = num_runs
        logger.debug(f"Benchmark for number of implementations {len(self.encryption_classes)},"
                     f" measured each operation {self.num_runs} times.")

    def run(self):
        """
        Measure time for operations in every iteration for every operation
        :return:
        """
        global_start = time.time()
        data_gen = DataGenerator()
        result = defaultdict(dict)
        plain_text_operations = list(get_operation_names(PlainTextOperations))
        logger.debug(f"Plaintext operations list: {plain_text_operations}")
        for enc in self.encryption_classes:
            class_object = enc()
            impl_name = str(enc.__name__)
            logger.debug(f"Current framework is: {impl_name}")
            result[impl_name] = defaultdict(list)
            for operation in get_operation_names(DefaultOperations):
                # 0. Get required functions dynamically
                operation_data = getattr(data_gen, operation, None)
                operation_function = getattr(class_object, operation, None)
                if not operation_function:
                    # Go to next operation if not implemented
                    logger.debug(f"Not found {operation} implemented for {impl_name} class")
                    continue
                if not operation_data:
                    # If data could not be generated got to next operation
                    continue
                # 1. Get and prepare data
                inputs, ground_truth = operation_data()
                if "int" in operation:
                    encryption_func = getattr(class_object, "encryption_int_from_encoding")
                elif "float" in operation:
                    encryption_func = getattr(class_object, "encryption_float_from_encoding")
                else:
                    logger.debug("Only encryption for int or float are supported. Skipping.")
                    continue
                # 1.1 Handle different number of argument
                if not isinstance(inputs, tuple):
                    inputs = (inputs,)
                # 1.2 Encrypt if required
                if operation not in plain_text_operations:
                    inputs = list(map(encryption_func, inputs))
                # 2. Run and measure time
                for i_run in range(self.num_runs):
                    start = time.time()
                    operation_function(*inputs)
                    end = time.time()
                    # 3. Save result
                    result[impl_name][operation].append(end - start)
            logger.debug(f"Finished framework : {impl_name}")
        global_end = time.time()
        global_delta = global_end - global_start
        logger.debug(f"Total benchmark time is {global_delta:.1f} seconds")
        return result
