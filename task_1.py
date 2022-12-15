import hashlib

""" (1): Определить алгоритм H, использовавшийся для формирования хеш-кода h для строки m. """

hash_algorythm: set = {'sha3_512', 'sha384', 'md5', 'sha256', 'sha3_256', 'sha3_224', 'sha512',
                       'blake2s', 'sha3_384', 'sha224', 'blake2b', 'sha1'}


def define_hash_algorythm(*, m: bytes, h: hex) -> str:
    for a in hashlib.algorithms_available:
        temp = hashlib.new(a)
        temp.update(m)
        if a == 'shake_256' or a == 'shake_128':
            for i in range(256):
                if temp.hexdigest(i) == h:
                    return a
        else:
            if temp.hexdigest() == h:
                return a
