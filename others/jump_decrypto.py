import json
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

"""
Windows

pip3 install -i https://mirrors.aliyun.com/pypi/simple/  gmssl, pycryptodomex
"""


def signer_decode(val: str):
    data = val.split(".")[1]
    data = data + "=" * (-len(data) % 4)
    return json.loads(base64.b64decode(data))


def process_key(key):
    """
    返回32 bytes 的key
    """
    if not isinstance(key, bytes):
        key = bytes(key, encoding='utf-8')

    if len(key) >= 32:
        return key[:32]

    return pad(key, 32)


class BaseCrypto:

    def encrypt(self, text):
        return base64.urlsafe_b64encode(
            self._encrypt(bytes(text, encoding='utf8'))).decode('utf8')

    def _encrypt(self, data: bytes) -> bytes:
        raise NotImplementedError

    def decrypt(self, text):
        return self._decrypt(
            base64.urlsafe_b64decode(bytes(text,
                                           encoding='utf8'))).decode('utf8')

    def _decrypt(self, data: bytes) -> bytes:
        raise NotImplementedError


class GMSM4EcbCrypto(BaseCrypto):

    def __init__(self, key):
        self.key = process_key(key)
        self.sm4_encryptor = CryptSM4()
        self.sm4_encryptor.set_key(self.key, SM4_ENCRYPT)

        self.sm4_decryptor = CryptSM4()
        self.sm4_decryptor.set_key(self.key, SM4_DECRYPT)

    def _encrypt(self, data: bytes) -> bytes:
        return self.sm4_encryptor.crypt_ecb(data)

    def _decrypt(self, data: bytes) -> bytes:
        return self.sm4_decryptor.crypt_ecb(data)


class AESCrypto:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key):
        if len(key) > 32:
            key = key[:32]
        self.key = self.to_16(key)

    @staticmethod
    def to_16(key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB)  # 初始化加密器

    def encrypt(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self.to_16(text))),
                   encoding='utf8').replace('\n', '')  # 加密

    def decrypt(self, text):
        aes = self.aes()
        return str(
            aes.decrypt(base64.decodebytes(bytes(
                text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密


class AESCryptoGCM:
    """
    使用AES GCM模式
    """

    def __init__(self, key):
        self.key = process_key(key)

    def encrypt(self, text):
        """
        加密text，并将 header, nonce, tag (3*16 bytes, base64后变为 3*24 bytes)
        附在密文前。解密时要用到。
        """
        header = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_GCM)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(
            bytes(text, encoding='utf-8'))

        result = []
        for byte_data in (header, cipher.nonce, tag, ciphertext):
            result.append(base64.b64encode(byte_data).decode('utf-8'))

        return ''.join(result)

    def decrypt(self, text):
        """
        提取header, nonce, tag并解密text。
        """
        metadata = text[:72]
        header = base64.b64decode(metadata[:24])
        nonce = base64.b64decode(metadata[24:48])
        tag = base64.b64decode(metadata[48:])
        ciphertext = base64.b64decode(text[72:])

        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)

        cipher.update(header)
        plain_text_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return plain_text_bytes.decode('utf-8')


def get_aes_crypto(key, mode='GCM'):
    if mode == 'ECB':
        a = AESCrypto(key)
    elif mode == 'GCM':
        a = AESCryptoGCM(key)
    return a


def get_gm_sm4_ecb_crypto(key):
    return GMSM4EcbCrypto(key)


class Crypto:

    def __init__(self, cryptoes):
        self.cryptoes = cryptoes

    @property
    def encryptor(self):
        return self.cryptoes[0]

    def encrypt(self, text):
        return self.encryptor.encrypt(text)

    def decrypt(self, text):
        for decryptor in self.cryptoes:
            try:
                origin_text = decryptor.decrypt(text)
                if origin_text:
                    # 有时不同算法解密不报错，但是返回空字符串
                    return origin_text
            except (TypeError, ValueError, UnicodeDecodeError, IndexError):
                continue


if __name__ == "__main__":
    # SECRET_KEY
    key = '5fuSCl7BRrxODUfY7l119Z1o8EskSiD6A7WftWZfUx8jN8LIW9'
    # private_key 或 password 在数据库里的值
    data = [
        'eyJhbGciOiJIUzI1NiJ9.IiNzNjE4VDkzNkAi.nIYh1-sizBc2U_Ap2aQtfWzYHiM1850xedJ-MprfWBU',
    ]
    crypto = Crypto([
        get_aes_crypto(key, mode='ECB'),
        get_aes_crypto(key, mode='GCM'),
        get_gm_sm4_ecb_crypto(key),
    ])
    for d in data:
        if d.count(".") == 2:
            print('by signer:', signer_decode(d))
        else:
            print('by crypto:', crypto.decrypt(d))