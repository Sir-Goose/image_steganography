import EncodeDecode


def bytes_to_bit_string(binary_data):
    # Convert a bytes object to a string of bits
    return ''.join(f'{byte:08b}' for byte in binary_data)


def bit_string_to_bytes(bit_string):
    # Convert a string of 1s and 0s to a bytes object.
    if not isinstance(bit_string, str):
        raise TypeError("Expected a string of 1s and 0s")
    if len(bit_string) % 8 != 0:
        raise ValueError("The bit string length must be a multiple of 8")
    return bytes(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))


def file_to_binary(filename):
    # Convert a file to its binary representation.
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data


def binary_to_file(binary_data, output_filename):
    # Write binary data to a file.
    with open(output_filename, 'wb') as file:
        file.write(binary_data)


def encode_file_in_image(file_name, image_filename):
    print("Converting image to array")
    rgb_array_2d_decimal = EncodeDecode.convert_image_to_array(image_filename)

    print("Converting array to binary")
    rgb_array_2d_binary = EncodeDecode.convert_decimal_array_to_binary(rgb_array_2d_decimal)

    print("Converting file to binary")
    # Convert file to binary
    binary_data = file_to_binary(file_name)

    print("Converting binary to string of bits")
    # Convert to string
    # Convert length of binary_data to a 32-bit binary string
    length_prefix = format(len(binary_data) * 8, '032b')

    binary_string = length_prefix + bytes_to_bit_string(binary_data)

    print("Adjusting least significant bit in image to encode file")
    rgb_array_2d_binary = EncodeDecode.adjust_least_significant_bit(rgb_array_2d_binary, binary_string)

    print("Converting binary array to decimal")
    rgb_array_2d_decimal = EncodeDecode.convert_binary_array_to_decimal(rgb_array_2d_binary)

    print("Converting decimal array back to image")
    img_new = EncodeDecode.convert_array_to_image(rgb_array_2d_decimal)
    img_new.save('test.png')


def decode_file_from_image(image_filename, output_filename):
    # Convert the image to an array of pixel values
    rgb_array_2d_decimal = EncodeDecode.convert_image_to_array(image_filename)
    rgb_array_2d_binary = EncodeDecode.convert_decimal_array_to_binary(rgb_array_2d_decimal)

    # Extract the least significant bits to get our encoded binary string
    decoded_bits = EncodeDecode.get_least_significant_bits_any(rgb_array_2d_binary)

    # Extract the original binary string length from the first 32 bits
    original_length = int(decoded_bits[:32], 2)

    # Trim the decoded_bits to only contain the original message
    decoded_bits = decoded_bits[32:32 + original_length]

    raw_bytes = bit_string_to_bytes(decoded_bits)
    binary_to_file(raw_bytes, output_filename)


encode_file_in_image('aaaaa.jpg', 'elon.jpeg')
decode_file_from_image('test.png', 'bbbbb.png')
