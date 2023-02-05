# PyCrypto as paliside demo uses it as base for wrapping to python
import pycrypto
import numpy as np


class PalisideHE:
    def __init__(self, n_float=8192, plain_degree_int=65537, scale=30,
                 coeff_mod_bit_sizes=(60, 30, 30, 30, 60)):  # , init_args, operation_list: set):
        # self.operation_list = operation_list

        # self.int_HE = Pyfhel(key_gen=True, context_params={'scheme': 'BFV', 'n': 2**13, 't': 65537, 'sec': 128,})

        # self.float_HE = Pyfhel(key_gen=True, context_params={'scheme': 'CKKS', 'n': 2**14, 'scale': 2**30, 'qi_sizes': [60, 30, 30, 30, 60]})
        self.float_HE = pycrypto.CKKSwrapper()
        self.batch_size = 100
        self.float_HE.KeyGen(1, scale, self.batch_size)
        # self.tmp_dir_float = tempfile.TemporaryDirectory() #for saving and restoring floats info
        # self.tmp_dir_name_float = self.tmp_dir_float.name

    # function to encode integers, so going from arr -> ptxt

    def encryption_float(self, arr):
        if isinstance(arr, float):
            arr = np.array([arr])
        arr = np.array(arr, dtype=np.float64)

        ctxt = self.float_HE.Encrypt(arr.tolist())

        return ctxt

    def encryption_float_from_encoding(self, arr):
        return self.encryption_float(arr)

    def addition_float(self, ctxt1,
                       ctxt2):  # to remember that to compute the operation the ctxt have to be built with the same context
        ccSum = self.float_HE.EvalAdd(ctxt1, ctxt2)
        return ccSum

    def multiplication_float(self, ctxt1,
                             ctxt2):  # to remember that to compute the operation the ctxt have to be built with the same context
        ccMul = self.float_HE.EvalMult(ctxt1, ctxt2)
        return ccMul

    def decrypt_float(self, ctxt):
        res = self.float_HE.Decrypt(ctxt)
        return res

    def scalar_product_float(self, arr1, arr2):
        multiply_pairs = self.float_HE.EvalMult(arr1, arr2)
        ccScPr = self.float_HE.EvalSum(multiply_pairs, self.batch_size)
        return ccScPr
