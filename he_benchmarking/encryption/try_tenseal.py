from tenseal_lib import TenSealHE
import numpy as np

example = TenSealHE()

a = example.encryption_float([3.7, 7.65])
b = example.encryption_float([4.6, 8.111])

sum = example.addition_float(a,b)
mult = example.multiplication_float(a,b)
dot = example.scalar_product_float(a,b)

context_bytes = example.save_in_bytes_int()
context = example.restore_from_bytes_int(context_bytes)

print(context)
# print(example.decrypt_float(dot))
