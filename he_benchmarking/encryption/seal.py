import numpy as np
from Pyfhel import Pyfhel


class SealHE:
    def __init__(self, init_args, operation_list: set):
        self.operation_list = operation_list
        
        self.int_HE = Pyfhel(key_gen=True, context_params={'scheme': 'BFV', 'n': 2**13, 't': 65537, 't_bits': 20, 'sec': 128,})
        
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
        self.float_He = Pyfhel()
        float_HE.contextGen(**ckks_params)  # Generate context for bfv scheme
        float_HE.keyGen()  # Key Generation: generates a pair of public/secret keys
        float_HE.rotateKeyGen()

    def encryption_int(self, arr):
        ptxt = int_HE.encodeInt(arr)
        ctxt = int_HE.encrypt(ctxt)
        return ctxt
    
    def addition_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccSum = ctxt1 + ctxt2
        return ccSum
    
    def multiplication_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccMul = ctxt1 * ctxt2
        return ccMul
    
    def relinearization_int(self, ctxt):
        rel_ctxt = int_HE.relinearize(ctxt)
        return rel_ctxt
    
    def decrypt_int(self, ctxt):
        res = int_HE.decryptInt(ctxt)
        return res
    
    def encription_float(self, args):
        return

    def addition_float(self, args):
        return

    def multiplication_float(self, args):
        return







