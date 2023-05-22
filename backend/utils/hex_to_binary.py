HEX_TO_BINARY_CONVERSION_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "a": "1010",
    "b": "1011",
    "c": "1100",
    "d": "1101",
    "e": "1110",
    "f": "1111",
}


def hex_to_binary(hex_string: str) -> str:
    """
    Converts a hexadecimal string to a binary string using a lookup table.

    Args:
        hex_string (str): The hexadecimal string to convert.

    Returns:
        str: The converted binary string.
    """
    binary_string = ""

    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[character]

    return binary_string


def main() -> None:
    """
    Main function to demonstrate the usage of hex_to_binary function.
    """
    number = 451
    hex_number = hex(number)[2:]
    print(f"hex_number: {hex_number}")

    binary_number = hex_to_binary(hex_number)
    print(f"binary_number: {binary_number}")


if __name__ == "__main__":
    main()
