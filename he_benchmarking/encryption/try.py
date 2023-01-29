from seal import SealHE
from Pyfhel import Pyfhel
import numpy as np
import copy


example = SealHE()

# pass two random integers to encrypt them
a = example.encryption_int(3)
b = example.encryption_int(4)

# sum the two values
res_sum = example.addition_int(a,b)
# print(a, "->", b, "->", res_sum)

# multiply the two values
res_mult = example.multiplication_int(a,b)
# print("result multiplication", res_mult)

# relinearization of the number after multiplying between two cypertexts 
copy_res_mult = copy.copy(res_mult)
example.relinearization_int(res_mult)
# print(copy_res_mult, "->", res_mult)

# decrypt the final results 
decr_res = example.decrypt_int(res_mult)
# print(decr_res) # the result can be found in the first position of the array
                #, the length of the array is equal to the parameter n in the creation of the Pyfhel object


# examples with integers to test the scalar product
c = example.encryption_int([2,3])
d = example.encryption_int([6,5])

res_mult = example.multiplication_int(c,d)
example.relinearization_int(res_mult)

scalar_prod = example.scalar_product_int(c,d) # the scalar product actually work, nevetheless there is some optimization that
                                            # regards the context parameters if the length of the array is too long, that I currently not implent
                                            
decr_res = example.decrypt_int(scalar_prod)
# print(decr_res)

dir = example.save_in_file_int(3)
example.restore_from_file_int(3)

context, public_key, secret_key, relin_key, rotate_key, c, p = example.save_in_bytes_int(3)
example.restore_from_bytes_int(context, public_key, secret_key, relin_key, rotate_key, c, p, 3)


e = example.encryption_float(2.75)
f = example.encryption_float(3.25)

res_sum = example.addition_float(e,f)

res_mult = example.multiplication_float(e,f)

copy_res_mult = copy.copy(res_mult)
example.relinearization_float(res_mult)
# print(copy_res_mult, "->", res_mult)

decr_res = example.decrypt_float(res_mult)
# print(decr_res)

g = example.encryption_float([2.5,3.3])
h = example.encryption_float([6.9,5.1])

res_mult = example.multiplication_float(g,h)
example.relinearization_float(res_mult)

scalar_prod = example.scalar_product_float(g,h) # the scalar product actually work, nevetheless there is some optimization that
                                            # regards the context parameters if the length of the array is too long, that I currently not implent
                                            
decr_res = example.decrypt_float(res_mult)
# print(decr_res)

dir = example.save_in_file_float(3.75)
example.restore_from_file_float(3.75)

context, public_key, secret_key, relin_key, rotate_key, c, p = example.save_in_bytes_float(4.334)
example.restore_from_bytes_float(context, public_key, secret_key, relin_key, rotate_key, c, p, 4.334)


## TRASH 
# arr = np.array(3)

# int_HE = Pyfhel(key_gen=True, context_params={'scheme': 'BFV', 'n': 2**13, 't': 65537, 't_bits': 20, 'sec': 128,})

# ptxt = int_HE.encodeInt(arr)
# ctxt = int_HE.encryptPtxt(ptxt)

# print(arr, "->", ptxt, "->", ctxt)


