from pygost import gost34112012256

fio = "Попов Николай Александрович"
fio_bytes = fio.encode("utf-8")
hash_result = gost34112012256.new(fio_bytes).digest()

print(hash_result)
variant_number = hash_result[-1] & 0x0F
print(variant_number)
