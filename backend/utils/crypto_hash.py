import hashlib
import json
from typing import Any


def crypto_hash(*args: Any) -> str:
    """
    Generate a sha-256 hash of the given arguments.

    Args:
        *args: Variable length argument list of any data type.

    Returns:
        str: The hexadecimal string representation of the sha-256 hash.
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = "".join(stringified_args)
    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()


def main() -> None:
    """
    Main function to demonstrate the usage of crypto_hash function.
    """
    print(f"crypto_hash: {crypto_hash('foo', ['sdsd'], 'asd')}")


if __name__ == "__main__":
    main()
