""" Вар. 2 """
import task_1
import task_2
import task_3_4

m: str = 'orange'
h: hex = '1b4c9133da73a711322404314402765ab0d23fd362a167d6f0c65bb215113d94'


def main():
    # Пункт 1
    m_bytes: bytes = bytes(m, 'utf-8')
    hash_name: str = task_1.define_hash_algorythm(m=m_bytes, h=h)
    print('Название алгоритма хеширования: {}'.format(hash_name))
    # Пункт 2
    key: bytes = task_2.key_calculation(hash_name=hash_name, password=m_bytes)
    print('Ключ с заданными параметрами: {}'.format(key.hex()))
    # Пункт 3 и 4
    task_3_4.start_session(code=key)
    task_3_4.encrypt(filepath_from='task_3_4/input/input.txt', filepath_to='task_3_4/cipher/encrypted_data.bin')
    task_3_4.decrypt(filepath_from='task_3_4/cipher/encrypted_data.bin', filepath_to='task_3_4/output/decrypted.txt', code=key)


if __name__ == '__main__':
    main()
