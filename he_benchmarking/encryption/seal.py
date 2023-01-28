import numpy as np
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import tempfile
import os

class SealHE:
    def __init__(self):#, init_args, operation_list: set):
        #self.operation_list = operation_list
        
        self.int_HE = Pyfhel(key_gen=True, context_params={'scheme': 'BFV', 'n': 2**13, 't': 65537, 't_bits': 20, 'sec': 128,})
        self.tmp_dir = tempfile.TemporaryDirectory() #for saving and restoring
        self.tmp_dir_name = self.tmp_dir.name
 
        
    def encode_int(self, arr):
        if isinstance(arr, int):
            arr = np.array([arr])
        arr = np.array(arr, dtype=np.int64)
        ptxt = self.int_HE.encodeInt(arr)
        
        return ptxt
        
    def encryption_int(self, arr):       
        ptxt = self.encode_int(arr)
        
        ctxt = self.int_HE.encryptPtxt(ptxt)
        return ctxt
    
    def addition_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccSum = self.int_HE.add(ctxt1, ctxt2, in_new_ctxt=True)
        return ccSum
    
    def multiplication_int(self, ctxt1, ctxt2):# to remember that to compute the operation the ctxt have to be built with the same context
        ccMul = self.int_HE.multiply(ctxt1, ctxt2, in_new_ctxt=True)
        return ccMul
    
    def relinearization_int(self, ctxt):
        self.int_HE.relinKeyGen()
        self.int_HE.relinearize(ctxt)
        return ctxt
    
    def decrypt_int(self, ctxt):
        res = self.int_HE.decryptInt(ctxt)
        return res
    
    def scalar_product(self, arr1, arr2):
        self.int_HE.rotateKeyGen()
        ccScPr = arr1 @ arr2
        return ccScPr
    
    def save_in_file(self, arr): #save all object into file
        self.int_HE.relinKeyGen()
        self.int_HE.rotateKeyGen()
        
        ctxt = self.encryption_int(arr)
        ptxt = self.encode_int(arr)
        
        self.int_HE.save_context(self.tmp_dir_name + "/context")
        self.int_HE.save_public_key(self.tmp_dir_name + "/pub.key")
        self.int_HE.save_secret_key(self.tmp_dir_name + "/sec.key")
        self.int_HE.save_relin_key(self.tmp_dir_name + "/relin.key")
        self.int_HE.save_rotate_key(self.tmp_dir_name + "/rotate.key")
        ctxt.save(self.tmp_dir_name + "/c.ctxt")
        ptxt.save(self.tmp_dir_name + "/p.ptxt")
        
        #print("\n\t".join(os.listdir(self.tmp_dir_name)))
        
        return self.tmp_dir_name
    
    def restore_from_file(self, arr):
        HE_f = Pyfhel() # Empty creation
        HE_f.load_context(self.tmp_dir_name + "/context")
        HE_f.load_public_key(self.tmp_dir_name + "/pub.key")
        HE_f.load_secret_key(self.tmp_dir_name + "/sec.key")
        HE_f.load_relin_key(self.tmp_dir_name + "/relin.key")
        HE_f.load_rotate_key(self.tmp_dir_name + "/rotate.key")
        c_f = PyCtxt(pyfhel=HE_f, fileName= self.tmp_dir_name + "/c.ctxt")
        p_f = PyPtxt(pyfhel=HE_f, fileName= self.tmp_dir_name + "/p.ptxt", scheme='bfv')

        assert HE_f.decryptInt(HE_f.encrypt(np.array([arr])))[0]==arr, "Incorrect encryption"
        assert HE_f.decryptInt(c_f)[0]==arr, "Incorrect decryption/ciphertext"
        assert HE_f.decodeInt(p_f)[0]==arr, "Incorrect decoding"
        assert HE_f.decryptInt(c_f >> 1)[1]==arr, "Incorrect Rotation"
        c_relin = c_f**2
        ~c_relin
        assert c_relin.size()==2, "Incorrect relinearization"
        print(" All checks passed! Loaded from files correctly")
        
        # Cleaning up temporary directory
        self.tmp_dir.cleanup()
        
    def save_in_bytes(self, arr):
        self.int_HE.relinKeyGen()
        self.int_HE.rotateKeyGen()

        ctxt = self.encryption_int(arr)
        ptxt = self.encode_int(arr)        
        
        s_context   = self.int_HE.to_bytes_context()
        s_public_key= self.int_HE.to_bytes_public_key()
        s_secret_key= self.int_HE.to_bytes_secret_key()
        s_relin_key = self.int_HE.to_bytes_relin_key()
        s_rotate_key= self.int_HE.to_bytes_rotate_key()
        s_c         = ctxt.to_bytes()
        s_p         = ptxt.to_bytes()
        
        return s_context, s_public_key, s_secret_key, s_relin_key, s_rotate_key, s_c, s_p
        
    def restore_from_bytes(self, context, p_key, s_key, rel_key, rot_key, c, p, arr):
        HE_b = Pyfhel()                 # Empty creation
        HE_b.from_bytes_context(context)
        HE_b.from_bytes_public_key(p_key)
        HE_b.from_bytes_secret_key(s_key)
        HE_b.from_bytes_relin_key(rel_key)
        HE_b.from_bytes_rotate_key(rot_key)
        c_b = PyCtxt(pyfhel=HE_b, bytestring= c)
        p_b = PyPtxt(pyfhel=HE_b, bytestring= p)
        
        assert HE_b.decryptInt(HE_b.encryptInt(np.array([arr], dtype=np.int64)))[0]==arr, "Incorrect encryption"
        assert HE_b.decryptInt(c_b)[0]==arr, "Incorrect decryption/ciphertext"
        assert HE_b.decodeInt(p_b)[0]==arr, "Incorrect decoding"
        assert HE_b.decryptInt(c_b >> 1)[1]==arr, "Incorrect Rotation"
        c_relin = c_b**2
        ~c_relin
        assert c_relin.size()==2, "Incorrect relinearization"
        print("  All checks passed! Loaded from bytestrings correctly")








