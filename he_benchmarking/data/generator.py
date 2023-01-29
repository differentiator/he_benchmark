import numpy as np

# DataGenerator class, which allows to randomly sample Integers and Floats and add them together.
# This will create a ground truth, which can be used for benchmarking HE performance.
# Parameters:
#   - low: Lower boundary for random samples (e.g. -10000)
#   - high: Higher boundary for random samples (e.g. 10000)
#   - seed: Random seed, which can be set to ensure reproducibility
# Python version: 3.10+ is needed, since the function "ground_truth" uses the match-case functionality.
class DataGenerator():

    def __init__(self, low, high, seed=None):
        self.low = low
        self.high = high
        self.seed = seed

        if seed is not None:
            np.random.seed(seed)
    
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

        return x1,x2

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
    def ground_truth(self, type, x1, x2):
        match type:
            case 0:
                return np.add(x1, x2)
            case 1:
                return np.subtract(x1, x2)
            case 2:
                return np.multiply(x1, x2)
            case 3:
                return np.divide(x1, x2)
            case 4:
                return np.dot(x1, x2)

