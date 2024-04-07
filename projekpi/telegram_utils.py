from pyrogram import Client, User
from pyrogram.errors import RPCError


class TelegramService:
    def __init__(self, nomor_telepon, name, api_id, api_hash):
        self.nomor_telepon = nomor_telepon
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash

    async def connection(self):
        self.app = Client(self.name, self.api_id, self.api_hash)

    def initial_auth(self, code) -> User:
        try:
            self.app.connect()

            sent_code = self.app.send_code(self.nomor_telepon)

            signed_in = self.app.sign_in(self.nomor_telepon, sent_code.phone_code_hash, code)

            if isinstance(signed_in, User):
                return signed_in
        except RPCError as e:
            raise e
        finally:
            self.app.disconnect()

    def send_message(self, destination, message):
        self.app.send_message(destination, message)
