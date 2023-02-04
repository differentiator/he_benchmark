import numpy as np
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import tempfile
import os
from math import isclose


class SealHE:
    def __init__(self):#, init_args, operation_list: set):
        #self.operation_list = operation_list
        
        self.int_HE = Pyfhel(key_gen=True, context_params={'scheme': 'BFV', 'n': 2**13, 't': 65537, 't_bits': 20, 'sec': 128,})
        # self.tmp_dir_int = tempfile.TemporaryDirectory() #for saving and restoring integers info
        # self.tmp_dir_name_int = self.tmp_dir_int.name
 
        self.float_HE = Pyfhel(key_gen=True, context_params={'scheme': 'CKKS', 'n': 2**14, 'scale': 2**30, 'qi_sizes': [60, 30, 30, 30, 60]})
        # self.tmp_dir_float = tempfile.TemporaryDirectory() #for saving and restoring floats info
        # self.tmp_dir_name_float = self.tmp_dir_float.name
        
        
    # function to encode integers, so going from arr -> ptxt    
    def encode_int(self, arr):
        if isinstance(arr, int):
            arr = np.array([arr])
        arr = np.array(arr, dtype=np.int64)
        ptxt = self.int_HE.encodeInt(arr)
        
        return ptxt
    
    def encode_float(self, arr):
        if isinstance(arr, float):
            arr = np.array([arr])
        arr = np.array(arr, dtype=np.float64)
        ptxt = self.float_HE.encodeFrac(arr)
        
        return ptxt
    
    # function to encrypt integers, going from ptxt -> ctxt
    def encryption_int_from_encoding(self, arr):       
        ptxt = self.encode_int(arr)
        
        ctxt = self.int_HE.encryptPtxt(ptxt)
        return ctxt
    
    def encryption_float_from_encoding(self, arr):       
        ptxt = self.encode_float(arr)
        
        ctxt = self.float_HE.encryptPtxt(ptxt)
        return ctxt
    
    def encryption_int(self, arr): #this operation are for comparison with the other library since we do not do this double passage encoding and encrypting every time
        if isinstance(arr, int):
            arr = np.array([arr])
        arr = np.array(arr, dtype=np.int64)       
        
        ctxt = self.int_HE.encrypt(arr)
        
        return ctxt
    
    def encryption_float(self, arr):
        if isinstance(arr, float):
            arr = np.array([arr])
        arr = np.array(arr, dtype=np.float64)    
        
        ctxt = self.float_HE.encrypt(arr)
        
        return ctxt
    
    def addition_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccSum = self.int_HE.add(ctxt1, ctxt2, in_new_ctxt=True)
        return ccSum
    
    def addition_float(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccSum = self.float_HE.add(ctxt1, ctxt2, in_new_ctxt=True)
        return ccSum
    
    def multiplication_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccMul = self.int_HE.multiply(ctxt1, ctxt2, in_new_ctxt=True)
        return ccMul
    
    def multiplication_float(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccMul = self.float_HE.multiply(ctxt1, ctxt2, in_new_ctxt=True)
        return ccMul
    
    def relinearization_int(self, ctxt):
        self.int_HE.relinKeyGen()
        self.int_HE.relinearize(ctxt)
        return ctxt

    def relinearization_float(self, ctxt):
        self.float_HE.relinKeyGen()
        self.float_HE.relinearize(ctxt)
        return ctxt
    
    def decrypt_int(self, ctxt):
        res = self.int_HE.decryptInt(ctxt)
        return res
    
    def decrypt_float(self, ctxt):
        res = self.float_HE.decryptFrac(ctxt)
        return res
    
    def scalar_product_int(self, arr1, arr2):
        self.int_HE.rotateKeyGen()
        ccScPr = arr1 @ arr2
        return ccScPr
    
    def scalar_product_float(self, arr1, arr2):
        self.float_HE.rotateKeyGen()
        ccScPr = arr1 @ arr2
        return ccScPr
    
    def save_in_bytes_int(self):#, arr):
        self.int_HE.relinKeyGen()
        self.int_HE.rotateKeyGen()

        # ctxt = self.encryption_int(arr)
        # ptxt = self.encode_int(arr)        
        
        s_context   = self.int_HE.to_bytes_context()
        s_public_key= self.int_HE.to_bytes_public_key()
        s_secret_key= self.int_HE.to_bytes_secret_key()
        s_relin_key = self.int_HE.to_bytes_relin_key()
        s_rotate_key= self.int_HE.to_bytes_rotate_key()
        # s_c         = ctxt.to_bytes()
        # s_p         = ptxt.to_bytes()
        
        return s_context, s_public_key, s_secret_key, s_relin_key, s_rotate_key#, s_c, s_p
    
    def save_in_bytes_float(self):#, arr):
        self.float_HE.relinKeyGen()
        self.float_HE.rotateKeyGen()

        # ctxt = self.encryption_float(arr)
        # ptxt = self.encode_float(arr)        
        
        s_context   = self.float_HE.to_bytes_context()
        s_public_key= self.float_HE.to_bytes_public_key()
        s_secret_key= self.float_HE.to_bytes_secret_key()
        s_relin_key = self.float_HE.to_bytes_relin_key()
        s_rotate_key= self.float_HE.to_bytes_rotate_key()
        # s_c         = ctxt.to_bytes()
        # s_p         = ptxt.to_bytes()
        
        return s_context, s_public_key, s_secret_key, s_relin_key, s_rotate_key#, s_c, s_p
        
    def restore_from_bytes_int(self, context, p_key, s_key, rel_key, rot_key):#, c, p, arr):
        HE_b = Pyfhel()  # Empty creation
        HE_b.from_bytes_context(context)
        HE_b.from_bytes_public_key(p_key)
        HE_b.from_bytes_secret_key(s_key)
        HE_b.from_bytes_relin_key(rel_key)
        HE_b.from_bytes_rotate_key(rot_key)
        # c_b = PyCtxt(pyfhel=HE_b, bytestring= c)
        # p_b = PyPtxt(pyfhel=HE_b, bytestring= p)
        
        # assert HE_b.decryptInt(HE_b.encryptInt(np.array([arr], dtype=np.int64)))[0]==arr, "Incorrect encryption"
        # assert HE_b.decryptInt(c_b)[0]==arr, "Incorrect decryption/ciphertext"
        # assert HE_b.decodeInt(p_b)[0]==arr, "Incorrect decoding"
        # assert HE_b.decryptInt(c_b >> 1)[1]==arr, "Incorrect Rotation"
        # c_relin = c_b**2
        # ~c_relin
        # assert c_relin.size()==2, "Incorrect relinearization"
        # print(" All checks passed! Integers info loaded from bytestrings correctly")
        
    def restore_from_bytes_float(self, context, p_key, s_key, rel_key, rot_key):#, c, p, arr):
        HE_b = Pyfhel()  # Empty creation
        HE_b.from_bytes_context(context)
        HE_b.from_bytes_public_key(p_key)
        HE_b.from_bytes_secret_key(s_key)
        HE_b.from_bytes_relin_key(rel_key)
        HE_b.from_bytes_rotate_key(rot_key)
        # c_b = PyCtxt(pyfhel=HE_b, bytestring= c)
        # p_b = PyPtxt(pyfhel=HE_b, bytestring= p)
        
        # assert isclose(HE_b.decryptFrac(HE_b.encrypt(np.array([arr])))[0], arr, abs_tol=1e-2), "Incorrect encryption"
        # assert isclose(HE_b.decryptFrac(c_b)[0], arr, abs_tol=1e-2), "Incorrect decryption/ciphertext"
        # assert isclose(HE_b.decodeFrac(p_b)[0], arr, abs_tol=1e-2), "Incorrect decoding"
        # assert isclose(HE_b.decryptFrac(c_b >> 1)[1], arr, abs_tol=1e-2), "Incorrect Rotation"
        # c_relin = c_b**2
        # ~c_relin
        # assert c_relin.size()==2, "Incorrect relinearization"
        # print(" All checks passed! Floats info loaded from bytestrings correctly")
        
    # #save all object into file
    # def save_in_file_int(self, arr): 
    #     self.int_HE.relinKeyGen()
    #     self.int_HE.rotateKeyGen()
        
    #     ctxt = self.encryption_int(arr)
    #     ptxt = self.encode_int(arr)
        
    #     self.int_HE.save_context(self.tmp_dir_name_int + "/context")
    #     self.int_HE.save_public_key(self.tmp_dir_name_int + "/pub.key")
    #     self.int_HE.save_secret_key(self.tmp_dir_name_int + "/sec.key")
    #     self.int_HE.save_relin_key(self.tmp_dir_name_int + "/relin.key")
    #     self.int_HE.save_rotate_key(self.tmp_dir_name_int + "/rotate.key")
    #     ctxt.save(self.tmp_dir_name_int + "/c.ctxt")
    #     ptxt.save(self.tmp_dir_name_int + "/p.ptxt")
        
    #     #print("\n\t".join(os.listdir(self.tmp_dir_name)))
        
    #     return self.tmp_dir_name_int
    
    # def save_in_file_float(self, arr): 
    #     self.float_HE.relinKeyGen()
    #     self.float_HE.rotateKeyGen()
        
    #     ctxt = self.encryption_float(arr)
    #     ptxt = self.encode_float(arr)
        
    #     self.float_HE.save_context(self.tmp_dir_name_float + "/context")
    #     self.float_HE.save_public_key(self.tmp_dir_name_float + "/pub.key")
    #     self.float_HE.save_secret_key(self.tmp_dir_name_float + "/sec.key")
    #     self.float_HE.save_relin_key(self.tmp_dir_name_float + "/relin.key")
    #     self.float_HE.save_rotate_key(self.tmp_dir_name_float + "/rotate.key")
    #     ctxt.save(self.tmp_dir_name_float + "/c.ctxt")
    #     ptxt.save(self.tmp_dir_name_float + "/p.ptxt")
        
    #     # print("\n\t".join(os.listdir(self.tmp_dir_name_float)))
        
    #     return self.tmp_dir_name_float
    
    # def restore_from_file_int(self, arr):
    #     HE_f = Pyfhel() # Empty creation
    #     HE_f.load_context(self.tmp_dir_name_int + "/context")
    #     HE_f.load_public_key(self.tmp_dir_name_int + "/pub.key")
    #     HE_f.load_secret_key(self.tmp_dir_name_int + "/sec.key")
    #     HE_f.load_relin_key(self.tmp_dir_name_int + "/relin.key")
    #     HE_f.load_rotate_key(self.tmp_dir_name_int + "/rotate.key")
    #     c_f = PyCtxt(pyfhel=HE_f, fileName= self.tmp_dir_name_int + "/c.ctxt")
    #     p_f = PyPtxt(pyfhel=HE_f, fileName= self.tmp_dir_name_int + "/p.ptxt", scheme='bfv')

    #     assert HE_f.decryptInt(HE_f.encrypt(np.array([arr])))[0]==arr, "Incorrect encryption"
    #     assert HE_f.decryptInt(c_f)[0]==arr, "Incorrect decryption/ciphertext"
    #     assert HE_f.decodeInt(p_f)[0]==arr, "Incorrect decoding"
    #     assert HE_f.decryptInt(c_f >> 1)[1]==arr, "Incorrect Rotation"
    #     c_relin = c_f**2
    #     ~c_relin
    #     assert c_relin.size()==2, "Incorrect relinearization"
    #     print(" All checks passed! Integers info loaded from files correctly")
        
    #     # Cleaning up temporary directory
    #     self.tmp_dir_int.cleanup()
        
    # def restore_from_file_float(self, arr):
    #     HE_f = Pyfhel() # Empty creation
    #     HE_f.load_context(self.tmp_dir_name_float + "/context")
    #     HE_f.load_public_key(self.tmp_dir_name_float + "/pub.key")
    #     HE_f.load_secret_key(self.tmp_dir_name_float + "/sec.key")
    #     HE_f.load_relin_key(self.tmp_dir_name_float + "/relin.key")
    #     HE_f.load_rotate_key(self.tmp_dir_name_float + "/rotate.key")
    #     c_f = PyCtxt(pyfhel=HE_f, fileName= self.tmp_dir_name_float + "/c.ctxt")
    #     p_f = PyPtxt(pyfhel=HE_f, fileName= self.tmp_dir_name_float + "/p.ptxt", scheme='ckks')

    #     assert isclose(HE_f.decryptFrac(HE_f.encrypt(np.array([arr])))[0], arr, abs_tol=1e-2), "Incorrect encryption"
    #     assert isclose(HE_f.decryptFrac(c_f)[0], arr, abs_tol=1e-2), "Incorrect decryption/ciphertext"
    #     assert isclose(HE_f.decodeFrac(p_f)[0], arr, abs_tol=1e-2), "Incorrect decoding"
    #     assert isclose(HE_f.decryptFrac(c_f >> 1)[1], arr, abs_tol=1e-2), "Incorrect Rotation"
    #     c_relin = c_f**2
    #     ~c_relin
    #     assert c_relin.size()==2, "Incorrect relinearization"
    #     print(" All checks passed! Floats info loaded from files correctly")
        
    #     # Cleaning up temporary directory
    #     self.tmp_dir_float.cleanup()







