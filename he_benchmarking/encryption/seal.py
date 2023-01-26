import numpy as np
from Pyfhel import Pyfhel

class SealHE:
    def __int__(self, init_args, operation_list: set):
        self.operation_list = operation_list
        self.int_HE = Pyfhel()  # Creating empty Pyfhel object
        self.int_HE.contextGen(scheme='bfv', n=2 ** 14, t_bits=20)  # Generate context for 'bfv'/'ckks' scheme
        # The n defines the number of plaintext slots.
        #  There are many configurable parameters on this step
        #  More info in Demo_2, Demo_3, and Pyfhel.contextGen()
        self.int_HE.keyGen()
        float_HE = Pyfhel()  # Creating empty Pyfhel object
        ckks_params = {
            'scheme': 'CKKS',  # can also be 'ckks'
            'n': 2 ** 14,  # Polynomial modulus degree. For CKKS, n/2 values can be
            #  encoded in a single ciphertext.
            #  Typ. 2^D for D in [10, 16]
            'scale': 2 ** 30,  # All the encodings will use it for float->fixed point
            #  conversion: x_fix = round(x_float * scale)
            #  You can use this as default scale or use a different
            #  scale on each operation (set in float_HE.encryptFrac)
            'qi_sizes': [60, 30, 30, 30, 60]  # Number of bits of each prime in the chain.
            # Intermediate values should be  close to log2(scale)
            # for each operation, to have small rounding errors.
        }
        float_HE.contextGen(**ckks_params)  # Generate context for bfv scheme
        float_HE.keyGen()  # Key Generation: generates a pair of public/secret keys
        float_HE.rotateKeyGen()

    def addition_int(self, args):
        return

    def addition_float(self, args):
        return
