import numpy as np


class dataGenerator():

    def __init__(self, low, high, seed=None):
        self.low = low
        self.high = high
        self.seed = seed

        if seed is not None:
            np.random.seed(seed)
    
    def getLow(self):
        return self.low
    
    def setLow(self, low):
        self.low = low

    def getHigh(self):
        return self.high
    
    def setHigh(self, high):
        self.high = high

    def getSeed(self):
        return self.seed
    
    def setSeed(self, seed):
        self.seed = seed

    def generateInts(self, size):
        x1 = np.random.randint(self.low, self.high, size=size)
        x2 = np.random.randint(self.low, self.high, size=size)

        return x1,x2

    def generateFloats(self, size):
        x1 = np.random.uniform(self.low, self.high, size=size)
        x2 = np.random.uniform(self.low, self.high, size=size)

        return x1, x2

    def ground_truth(self, x1, x2):
        return np.add(x1, x2)


