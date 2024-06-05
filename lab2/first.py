from math import sqrt



def eratosthenes(n):     # n - число, до которого хотим найти простые числа 
    sieve = list(range(n + 1))
    sieve[1] = 0    # без этой строки итоговый список будет содержать единицу
    for i in sieve:
        if i > 1:
            for j in range(2*i, len(sieve), i):
                sieve[j] = 0
    return sieve


my_number = 383456614884902466726252731294544234658015390619372835826246625499154384118189
# print(int(sqrt(my_number)))


primes = eratosthenes(10 ** 9)


# for prime in primes:
#     if prime != 0 and my_number % prime == 0:
#         print(prime)
#         break
