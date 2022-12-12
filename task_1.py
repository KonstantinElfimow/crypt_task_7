import hashlib

""" (1): Определить алгоритм H, использовавшийся для формирования хеш-кода h для строки m. """


hash_algorythm: list = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'md5']


def define_hash_algorythm(*, m: bytes, h: hex) -> str:
    for a in hash_algorythm:
        temp = hashlib.new(a)
        temp.update(m)
        if temp.hexdigest() == h:
            return a
    return None
