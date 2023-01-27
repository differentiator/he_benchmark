import numpy as np

# DataGenerator class, which allows to randomly sample Integers and Floats and add them together.
# This will create a ground truth, which can be used for benchmarking HE performance.
# Parameters:
#   - low: Lower boundary for random samples (e.g. -10000)
#   - high: Higher boundary for random samples (e.g. 10000)
#   - seed: Random seed, which can be set to ensure reproducibility
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

    # Function for generating the ground truth of combining the two randomly generated numpy arrays. The type of operation needs to be specified through "type".
    # Options for "type":
    #   - "add": Addition
    #   - "sub": Subtraction
    #   - "mul": Multiplication
    #   - "div": Division
    def ground_truth(self, type, x1, x2):
        match type:
            case "add":
                return np.add(x1, x2)
            case "sub":
                return np.subtract(x1, x2)
            case "mul":
                return np.multiply(x1, x2)
            case "div":
                return np.divide(x1, x2)





