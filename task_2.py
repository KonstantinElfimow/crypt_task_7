import hashlib
import datetime

""" (2): С использованием алгоритма PKCS5_PBKDF2 вычислить значение ключа K
для строки пароля, совпадающей со значением m из задачи (1), и строки соли s,
задавемой текущей (на момент сдачи задачи) датой в формате yyyy-mm-dd. Число
итераций алгоритма PKCS5_PBKDF2 – 4096, используемая внутри алгоритма
PKCS5_PBKDF2 хеш-функция должна совпадать с H из задачи (1). Ожидаемая длина
ключа K – 256 бит. """

iterations: int = 4096
key_len: int = 32  # Размер в байтах


def key_calculation(*, hash_name: str, password: bytes) -> bytes:
    now = datetime.datetime.now()
    salt: bytes = bytes(now.strftime('%Y/%m/%d'), 'utf-8')
    return hashlib.pbkdf2_hmac(hash_name=hash_name, password=password, salt=salt, iterations=iterations, dklen=key_len)
