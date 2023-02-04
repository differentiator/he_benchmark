import numpy as np
import inspect


def get_operation_names(class_obj):
    for i in inspect.getmembers(class_obj):
        # to remove private and protected
        # functions
        if not i[0].startswith('_'):
            # To remove other methods that
            # doesnot start with an underscore
            if not inspect.ismethod(i[1]):
                yield i[0]


# DataGenerator class, which allows to randomly sample Integers and Floats and add them together.
# This will create a ground truth, which can be used for benchmarking HE performance.
# Parameters:
#   - low: Lower boundary for random samples (e.g. -10000)
#   - high: Higher boundary for random samples (e.g. 10000)
#   - seed: Random seed, which can be set to ensure reproducibility
# Python version: 3.10+ is needed, since the function "ground_truth" uses the match-case functionality.
class DataGenerator:

    def __init__(self, low=-20000, high=20000, size=10, seed=None):
        self.low = low
        self.high = high
        self.size = size
        self.seed = seed

        if seed is not None:
            np.random.seed(seed)

        self.x1_int, self.x2_int = self.generateInts(size)
        self.x1_float, self.x2_float = self.generateFloats(size)

    # Get function for lower boundary
    def getLow(self):
        return self.low

    # Set function for lower boundary 
    def setLow(self, low):
        self.low = low

    # Get function for higher boundary
    def getHigh(self):
        return self.high

    # Set function for higher boundary
    def setHigh(self, high):
        self.high = high

    # Get function for random seed
    def getSeed(self):
        return self.seed

    # Set function for random seed
    def setSeed(self, seed):
        self.seed = seed

    # Function for generating Integers. The number of Integers that should be generated needs to be specified through "size".
    # Returns two numpy arrays (x1,x2) with length "size" of randomly generated Integers between the lower and higher boundary.
    def generateInts(self, size):
        x1 = np.random.randint(self.low, self.high, size=size)
        x2 = np.random.randint(self.low, self.high, size=size)

        return x1, x2

    # Function for generating Floats. The number of Floats that should be generated needs to be specified through "size".
    # Returns two numpy arrays (x1,x2) with length "size" of randomly generated Floats between the lower and higher boundary.
    def generateFloats(self, size):
        x1 = np.random.uniform(self.low, self.high, size=size)
        x2 = np.random.uniform(self.low, self.high, size=size)

        return x1, x2

    # Function for generating the ground truth of combining two randomly generated numpy arrays. The type of operation needs to be specified through "type".
    # Options for "type":
    #   - 0: Addition
    #   - 1: Subtraction
    #   - 2: Multiplication
    #   - 3: Division
    #   - 4: Scalar product
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
