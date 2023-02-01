import tenseal as ts
import numpy as np

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import tempfile
import os
from math import isclose

class TenSealHE:
    def __init__(self):#, init_args, operation_list: set):
        #self.operation_list = operation_list
        
        self.int_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
        # self.int_context.auto_relin(False)
        self.int_context.generate_galois_keys() #what is it
        
        poly_mod_degree = 2**14
        coeff_mod_bit_sizes = [60, 30, 30, 30, 60]
        self.float_context = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
        # self.float_context.auto_relin(False)
        self.float_context.global_scale = 2**30
        self.float_context.generate_galois_keys()
    
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
    
    def addition_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_add = ctxt1 + ctxt2
        return encrypted_add
    
    def addition_float(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_add = ctxt1 + ctxt2
        return encrypted_add
    
    def multiplication_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_mul = ctxt1 * ctxt2        
        return encrypted_mul
    
    def multiplication_float(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        encrypted_mul = ctxt1.mul(ctxt2)
        return encrypted_mul
    
    def relinearization_int(self, ctxt):
        self.int_HE.relinKeyGen()
        self.int_HE.relinearize(ctxt)
        return ctxt

    def relinearization_float(self, ctxt):
        self.float_HE.relinKeyGen()
        self.float_HE.relinearize(ctxt)
        return ctxt
    
    def decrypt_int(self, ctxt):
        res = ctxt.decrypt()
        return res
    
    def decrypt_float(self, ctxt):
        res = ctxt.decrypt()
        return res
    
    def scalar_product_int(self, arr1, arr2):
        ccScPr = arr1.dot(arr2)
        return ccScPr
    
    def scalar_product_float(self, arr1, arr2):
        ccScPr = arr1.dot(arr2)
        return ccScPr
        
    def save_in_bytes_int(self):
        bytes = self.int_context.serialize()
        
        return bytes
    
    def save_in_bytes_float(self, arr):
        bytes = self.float_context.serialize()
        
        return bytes
        
    def restore_from_bytes_int(self, bytes):
        bytes_context = ts.context(data = ts.context().load(bytes))
        
        return bytes_context
        
    def restore_from_bytes_float(self, context, p_key, s_key, rel_key, rot_key, c, p, arr):
        HE_b = Pyfhel()  # Empty creation
        HE_b.from_bytes_context(context)
        HE_b.from_bytes_public_key(p_key)
        HE_b.from_bytes_secret_key(s_key)
        HE_b.from_bytes_relin_key(rel_key)
        HE_b.from_bytes_rotate_key(rot_key)
        c_b = PyCtxt(pyfhel=HE_b, bytestring= c)
        p_b = PyPtxt(pyfhel=HE_b, bytestring= p)
        
        assert isclose(HE_b.decryptFrac(HE_b.encrypt(np.array([arr])))[0], arr, abs_tol=1e-2), "Incorrect encryption"
        assert isclose(HE_b.decryptFrac(c_b)[0], arr, abs_tol=1e-2), "Incorrect decryption/ciphertext"
        assert isclose(HE_b.decodeFrac(p_b)[0], arr, abs_tol=1e-2), "Incorrect decoding"
        assert isclose(HE_b.decryptFrac(c_b >> 1)[1], arr, abs_tol=1e-2), "Incorrect Rotation"
        c_relin = c_b**2
        ~c_relin
        assert c_relin.size()==2, "Incorrect relinearization"
        print(" All checks passed! Floats info loaded from bytestrings correctly")
