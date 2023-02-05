import tenseal as ts
import numpy as np

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import tempfile
import os
from math import isclose


class TenSealHE:
    def __init__(self, n_int=4096, plain_degree_int=65537,
                 n_float=8192, scale=2 ** 30,
                 coeff_mod_bit_sizes=(60, 30, 30, 30, 60)):  # , init_args, operation_list: set):
        # self.operation_list = operation_list
        # self.int_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)

        self.int_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=n_int, plain_modulus=plain_degree_int)
        self.int_context.auto_relin = True  # False
        self.int_context.generate_galois_keys()  # what is it

        # poly_mod_degree = 2**14
        # coeff_mod_bit_sizes = [60, 30, 30, 30, 60]
        # self.float_context = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
        # self.float_context.auto_relin= True#False
        # self.float_context.global_scale = 2**30
        # self.float_context.generate_galois_keys()

        self.float_context = ts.context(scheme=ts.SCHEME_TYPE.CKKS, poly_modulus_degree=n_float,
                                        coeff_mod_bit_sizes=coeff_mod_bit_sizes)
        self.float_context.auto_relin = True  # False
        self.float_context.global_scale = scale
        self.float_context.generate_galois_keys()

    # compared with Pyfhel, Tenseal doesn't require this double passage of encoding and encrypting
    # function to encrypt integers, going from arr -> ctxt
    def encryption_int(self, arr):
        if isinstance(arr, int):
            arr = np.array([arr])
        encrypted_vector = ts.bfv_vector(self.int_context, arr)

        return encrypted_vector

    def encryption_float(self, arr):
        if isinstance(arr, float):
            arr = np.array([arr])
        encrypted_vector = ts.ckks_vector(self.float_context, arr)

        return encrypted_vector

    def encryption_float_from_encoding(self, arr):
        return self.encryption_float(arr)

    def encryption_int_from_encoding(self, arr):
        return self.encryption_int(arr)

    def addition_int(self, ctxt1,
                     ctxt2):  # to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_add = ctxt1 + ctxt2
        return encrypted_add

    def addition_float(self, ctxt1,
                       ctxt2):  # to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_add = ctxt1 + ctxt2
        return encrypted_add

    def multiplication_int(self, ctxt1,
                           ctxt2):  # to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_mul = ctxt1 * ctxt2
        return encrypted_mul

    def multiplication_float(self, ctxt1,
                             ctxt2):  # to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_mul = ctxt1.mul(ctxt2)
        return encrypted_mul

    # def relinearization_int(self, ctxt):
    #     self.int_HE.relinKeyGen()
    #     self.int_HE.relinearize(ctxt)
    #     return ctxt

    # def relinearization_float(self, ctxt):
    #     self.float_HE.relinKeyGen()
    #     self.float_HE.relinearize(ctxt)
    #     return ctxt

    def decrypt_int(self, ctxt):
        res = ctxt.decrypt()
        return res

    def decrypt_float(self, ctxt):
        res = ctxt.decrypt()
        return res

    def scalar_product_int(self, arr1, arr2):
        # self.int_context.auto_relin = True
        ccScPr = arr1.dot(arr2)
        # self.int_context.auto_relin = False

        return ccScPr

    def scalar_product_float(self, arr1, arr2):
        # self.float_context.auto_relin = True
        ccScPr = arr1.dot(arr2)
        # self.float_context.auto_relin = False

        return ccScPr

    def save_in_bytes_int(self):
        bytes = self.int_context.serialize(save_secret_key=True)

        return bytes

    def save_in_bytes_float(self):
        bytes = self.float_context.serialize(save_secret_key=True)

        return bytes

    def restore_from_bytes_int(self, bytes):
        bytes_context = ts.Context.load(bytes)

        return bytes_context

    def restore_from_bytes_float(self, bytes):
        bytes_context = ts.Context.load(bytes)

        return bytes_context
