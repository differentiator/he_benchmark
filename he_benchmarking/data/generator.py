import numpy as np


class dataGenerator():

    def __init__(self, low, high):
        self.low = low
        self.high = high
    
    def getLow(self):
        return self.low
    
    def setLow(self, low):
        self.low = low

    def getHigh(self):
        return self.high
    
    def setHigh(self, high):
        self.high = high

    def generate_int_data(self, size):
        x1 = np.random.randint(self.low, self.high, size=size)
        x2 = np.random.randint(self.low, self.high, size=size)

        return x1,x2

    def generate_float_data(self, size):
        x1 = np.random.uniform(self.low, self.high, size=size)
        x2 = np.random.uniform(self.low, self.high, size=size)

        return x1, x2

    def ground_truth(self, x1, x2):
        return np.add(x1, x2)




