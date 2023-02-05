import numpy as np
import inspect

from utils.logging import logger


def get_operation_names(class_obj):
    """
    Get operations from class attributes
    Args:
        class_obj:

    Returns:
        generator, each entry is an operation
    """
    for i in inspect.getmembers(class_obj):
        # to remove private and protected
        # functions
        if not i[0].startswith('_'):
            # To remove other methods that
            # does not start with an underscore
            if not inspect.ismethod(i[1]):
                yield i[0]


class DataGenerator:
    """
    DataGenerator class, which allows to randomly sample Integers and Floats and add them together.
    This will create a ground truth, which can be used for benchmarking HE performance.
    Parameters:
       - low: Lower boundary for random samples (e.g. -10000)
       - high: Higher boundary for random samples (e.g. 10000)
       - seed: Random seed, which can be set to ensure reproducibility
     Python version: 3.10+ is needed, since the function "ground_truth" uses the match-case functionality.
    """

    def __init__(self, low=-20000, high=20000, size=100, seed=None):
        self.low = low
        self.high = high
        self.size = size
        self.seed = seed

        if seed is not None:
            np.random.seed(seed)

        logger.debug("Starting generation of the data")
        self.x1_int, self.x2_int = self.generate_ints(size)
        self.x1_float, self.x2_float = self.generate_floats(size)

    # Get function for lower boundary
    def get_low(self):
        return self.low

    # Set function for lower boundary 
    def set_low(self, low):
        self.low = low

    # Get function for higher boundary
    def get_high(self):
        return self.high

    #
    def set_high(self, high):
        self.high = high

    # Get function for random seed
    def get_seed(self):
        return self.seed

    # Set function for random seed
    def set_seed(self, seed):
        self.seed = seed

    def generate_ints(self, size):
        """
        Function for generating Integers.
        The number of Integers that should be generated needs to be specified through "size".
        Returns two numpy arrays (x1,x2)
        with length "size" of randomly generated Integers between the lower and higher boundary.
        Args:
            size:

        Returns:

        """
        x1 = np.random.randint(self.low, self.high, size=size)
        x2 = np.random.randint(self.low, self.high, size=size)

        return x1, x2

    #
    def generate_floats(self, size):
        """
        Function for generating Floats.
        The number of Floats that should be generated needs to be specified through "size".
        Returns two numpy arrays (x1,x2)
        with length "size" of randomly generated Floats between the lower and higher boundary.
        Args:
            size:

        Returns:

        """
        x1 = np.random.uniform(self.low, self.high, size=size)
        x2 = np.random.uniform(self.low, self.high, size=size)

        return x1, x2

    # Functions for generating the ground truth and inputs for combining one/two randomly generated numpy arrays.
    # Possible operations:
    # 0. Addition
    # 1. Subtraction
    # 2. Multiplication
    # 3. Division
    # 4. Scalar product
    # 5. Encoding
    # 6. Encoding

    def encode_int(self):
        return self.x1_int, None

    def encode_float(self):
        return self.x1_float, None

    def encryption_int_from_encoding(self):
        return self.x1_int, None

    def encryption_float_from_encoding(self):
        return self.x1_float, None

    def addition_int(self):
        return (self.x1_int, self.x2_int), np.add(self.x1_int, self.x2_int)

    def addition_float(self):
        return (self.x1_float, self.x2_float), np.add(self.x1_float, self.x2_float)

    def multiplication_int(self):
        return (self.x1_int, self.x2_int), np.multiply(self.x1_int, self.x2_int)

    def multiplication_float(self):
        return (self.x1_float, self.x2_float), np.multiply(self.x1_float, self.x2_float)

    def relinearization_int(self):
        return self.x1_int, None

    def relinearization_float(self):
        return self.x1_float, None

    def decrypt_int(self):
        return self.x1_int, self.x1_int

    def decrypt_float(self):
        return self.x1_float, self.x1_float

    def scalar_product_int(self):
        return (self.x1_int, self.x2_int), np.dot(self.x1_int, self.x2_int)

    def scalar_product_float(self):
        return (self.x1_float, self.x2_float), np.dot(self.x1_float, self.x2_float)
