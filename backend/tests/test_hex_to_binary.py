from backend.utils.hex_to_binary import hex_to_binary


def test_hex_to_binary() -> None:
    """
    Tests the hex_to_binary function. It verifies that the binary representation of a
    hexadecimal number matches the binary representation of the original number.
    """
    original_number = 789
    hex_number = hex(original_number)[2:]
    binary_number = hex_to_binary(hex_number)
    assert original_number == int(binary_number, 2)
