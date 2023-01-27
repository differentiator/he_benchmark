import numpy as np


class dataGenerator:

    def generate_int_data(size):
        x1 = np.random.randint(-1000000,1000000,size=size)
        x2 = np.random.randint(-1000000,1000000,size=size)
        y = np.add(x1,x2)

        return x1,x2,y

    def generate_float_data(size):
        x1 = np.random.uniform(-100,100,size=size)
        x2 = np.random.uniform(-100,100,size=size)
        y = np.add(x1,x2)

        return x1,x2,y