from tenseal_lib import TenSealHE
import numpy as np

example = TenSealHE()

a = example.encryption_int(3)
b = example.encryption_int(4)

res_sum = example.addition_int(a,b)
print("sum: ", res_sum)

res_mult = example.multiplication_int(a,b)
print("multiplication: ", res_mult)

decr_res = example.decrypt_int(res_mult)
print("decryption of standard multiplication: ",decr_res)
print("type of the multiplication: ", type(decr_res))

c = example.encryption_int([2,3])
d = example.encryption_int([6,5])

scalar_prod = example.scalar_product_int(c,d)
decr_res = example.decrypt_int(scalar_prod)
print("decryption of scalar product: ",decr_res)
print("type of the scalar product: ", type(decr_res))

context_bytes = example.save_in_bytes_int()
context = example.restore_from_bytes_int(context_bytes)

e = example.encryption_float(2.75)
f = example.encryption_float(3.25)

res_sum = example.addition_float(e,f)
print("sum: ", res_sum)

res_mult = example.multiplication_float(e,f)
print("multiplication: ", res_mult)

decr_res = example.decrypt_float(res_mult)
print("decryption: of standard multiplication(float): ",decr_res)
print("type of the standard multiplication(float): ", type(decr_res))

g = example.encryption_float([2.5,3.3])
h = example.encryption_float([6.9,5.1])

scalar_prod = example.scalar_product_float(g,h)
decr_res = example.decrypt_float(scalar_prod)
print("decryption of scalar product(float): ",decr_res)
print("type of the scalar product(float): ", type(decr_res))

context_bytes = example.save_in_bytes_float()
context = example.restore_from_bytes_float(context_bytes)


## TRASH

# example.int_context.generate_relin_keys()

# print(context)
# print(example.decrypt_float(mult))
