from backend.utils.crypto_hash import crypto_hash


def test_crypto_hash():
    """
    Tests the crypto_hash function with various inputs. It checks whether the function
    returns consistent hashes for arguments of different data types in any order.
    It also verifies the correctness of the hash value for a known input.
    """
    assert crypto_hash(1, [2], "three") == crypto_hash(1, "three", [2])
    assert crypto_hash("foo") == "b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b"
