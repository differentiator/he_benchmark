import numpy as np


class dataGenerator():

    def generate_int_data(self, size):
        x1 = np.random.randint(-1000000,1000000,size=size)
        x2 = np.random.randint(-1000000,1000000,size=size)

        return x1,x2

    def generate_float_data(self, size):
        x1 = np.random.uniform(-100,100,size=size)
        x2 = np.random.uniform(-100,100,size=size)

        return x1, x2

    def ground_truth(self, x1, x2):
        return np.add(x1, x2)