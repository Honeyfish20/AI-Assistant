
from Cryptodome.Cipher import AES
import hashlib
import json
import base64
import aiohttp
import requests

class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')


class TokenManager():
    def __init__(self, app_id, app_secret) -> None:
        self.token = 'an_invalid_token'
        self.url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        self.req = {
            "app_id": app_id,
            "app_secret": app_secret
        }

    async def update(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers={
                'Content-Type': 'application/json; charset=utf-8'
            }, data=json.dumps(self.req), timeout=5) as response:
                data = await response.json()
                if (data["code"] == 0):
                    self.token = data["tenant_access_token"]

    async def get_token(self):
        return self.token


class LarkMsgSender():
    def __init__(self, token_manager: TokenManager) -> None:
        self.prefix = "https://open.feishu.cn/open-apis/im/v1/messages/"
        self.token_manager = token_manager

    async def update_card(self, msg, msg_id):
        url = self.prefix + msg_id
        headers = {
            'Authorization': 'Bearer ' + await self.token_manager.get_token(),  # your access token
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, headers=headers, data=json.dumps({
                "msg_type": "interactive",
                "content": json.dumps(
                    {
                        "config": {},
                            "i18n_elements": {
                                "zh_cn": [
                                    {
                                        "tag": "markdown",
                                        "content": msg
                                    }
                                ]
                            },
                            "i18n_header": {}      
                    }
                )
            })) as response:
                data = await response.json()
        if (data["code"] == 99991668 or data["code"] == 99991663):  # token expired
            await self.token_manager.update()
            await self.update_card(msg, msg_id)
        elif (data["code"] == 0):
            return 'Error'
        
    async def get_card_id(self, user_id):
        url = self.prefix + '?receive_id_type=user_id'
        headers = {
            'Authorization': 'Bearer ' + await self.token_manager.get_token(),  # your access token
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps({
                "receive_id": user_id,
                "msg_type": "interactive",
                "content": json.dumps(
                    {
                        "config": {},
                            "i18n_elements": {
                                "zh_cn": [
                                    {
                                        "tag": "markdown",
                                        "content": ""
                                    }
                                ]
                            },
                            "i18n_header": {}
                    }
                )
            })) as response:
                data = await response.json()
                       
        if (data["code"] == 99991668 or data["code"] == 99991663):  # token expired
            await self.token_manager.update()
            return await self.get_card_id(user_id)
        elif (data["code"] == 0):
            return data["data"]["message_id"]
       