import json
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from backend.config import STARTING_BALANCE


class Wallet:
    def __init__(self) -> None:
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend)
        self.public_key = self.private_key.public_key()

    def sign(self, data) -> bytes:
        return self.private_key.sign(json.dumps(data).encode("utf-8"), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify(public_key, data, signature):
        try:
            public_key.verify(
                signature, json.dumps(data).encode("utf-8"), ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f"Wallet: {wallet.__dict__}")

    data = {"foo": "bar"}
    signature = wallet.sign(data)
    print(f"signature: {signature}")


if __name__ == "__main__":
    main()
