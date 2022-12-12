from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

""" (3)-(4): Реализовать программный модуль, позволяющий шифровать / расшифровывать
пользовательские файлы с использованием одного из известных блочных
симметричных алгоритмов (и в моём случае ещё асимметричных). """


def start_session(*, code) -> None:
    """ Генерация ключей RSA public / private """
    key = RSA.generate(2048)

    encrypted_key = key.exportKey(
        passphrase=code,
        pkcs=8,
        protection="scryptAndAES128-CBC"
    )

    with open('task_3_4/my_private_rsa_key.bin', 'wb') as f:
        f.write(encrypted_key)

    with open('task_3_4/my_rsa_public.pem', 'wb') as f:
        f.write(key.publickey().exportKey())


def encrypt(*, filepath_from: str, filepath_to: str) -> None:
    """ Шифрование """
    # Мы открываем файл для записи. Далее, мы импортируем наш публичный ключ в переменной и создаем 16-битный
    # ключ сессии. Для этого примера мы будем использовать гибридный метод шифрования, так что мы используем PKCS#1
    # OAEP (Optimal asymmetric encryption padding). Это позволяет нам записывать данные произвольной длинны в файл.
    # Далее, мы создаем наш шифр AES, создаем кое-какие данные и шифруем их. Это дает нам зашифрованный текст и MAC.
    # Наконец, мы выписываем nonce, MAC (или тег), а также зашифрованный текст. К слову, nonce – это произвольное
    # число, которое используется только в криптографических связях. Обычно это случайные или псевдослучайные числа.
    # Для AES, оно должно быть минимум 16 байтов в ширину.
    with open(filepath_to, 'wb') as out_file:
        recipient_key = RSA.import_key(
            open('task_3_4/my_rsa_public.pem').read()
        )

        session_key = get_random_bytes(16)

        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        out_file.write(cipher_rsa.encrypt(session_key))

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        data = open(filepath_from, 'rb').read()
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)

        out_file.write(cipher_aes.nonce)
        out_file.write(tag)
        out_file.write(ciphertext)


def decrypt(*, filepath_from: str, filepath_to: str, code: hex) -> None:
    """ Дешифрование """
    # В данном случае, мы открываем наш зашифрованный файл для чтения в бинарном режиме. Далее, мы импортируем наш
    # приватный ключ. Внимание на то, что когда мы импортируем приватный ключ, мы должны передать ему код
    # доступа. В противном случае возникнет ошибка. Далее мы считываем наш файл. Сначала мы
    # считываем приватный ключ, затем 16 байтов для nonce, за которыми следуют 16 байтов, которые являются тегом,
    # и наконец, остальную часть файла, который и является нашими данными. Далее нам нужно расшифровать наш ключ
    # сессии, пересоздать наш ключ AES и расшифровать данные.
    with open(filepath_from, 'rb') as fobj:
        private_key = RSA.import_key(
            open('task_3_4/my_private_rsa_key.bin').read(),
            passphrase=code
        )

        enc_session_key, nonce, tag, ciphertext = [
            fobj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
        ]

        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        open(filepath_to, 'wb').write(data)
