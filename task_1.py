import hashlib

""" (1): Определить алгоритм H, использовавшийся для формирования хеш-кода h для строки m. """

hash_algorythm: set = {'sha3_512', 'sha384', 'md5', 'sha256', 'sha3_256', 'sha3_224', 'sha512',
                       'blake2s', 'sha3_384', 'sha224', 'blake2b', 'sha1'}


def define_hash_algorythm(*, m: bytes, h: hex) -> str:
    for a in hash_algorythm:
        temp = hashlib.new(a)
        temp.update(m)
        if temp.hexdigest() == h:
            return a
    return None
