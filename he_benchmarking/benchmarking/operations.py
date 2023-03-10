class DefaultOperations:
    """
    Config class with list of operations for which to measure time
    Input will be encrypted before
    """
    encode_int = "encode_int"
    encode_float = "encode_float"
    encryption_int_from_encoding = "encryption_int_from_encoding"
    encryption_float_from_encoding = "encryption_float_from_encoding"
    # encryption_int = "encryption_int"
    # encryption_float = "encryption_float"
    addition_int = "addition_int"
    addition_float = "addition_float"
    multiplication_int = "multiplication_int"
    multiplication_float = "multiplication_float"
    relinearization_int = "relinearization_int"
    relinearization_float = "relinearization_float"
    decrypt_int = "decrypt_int"
    decrypt_float = "decrypt_float"
    scalar_product_int = "scalar_product_int"
    scalar_product_float = "scalar_product_float"
    save_in_bytes_int = "save_in_bytes_int"
    save_in_bytes_float = "save_in_bytes_float"
    restore_from_bytes_int = "restore_from_bytes_int"
    restore_from_bytes_float = "restore_from_bytes_float"


class PlainTextOperations:
    """
    Config class with list of operations for which to measure time without encryption
    """
    encode_int = "encode_int"
    encode_float = "encode_float"
    encryption_int_from_encoding = "encryption_int_from_encoding"
    encryption_float_from_encoding = "encryption_float_from_encoding"

