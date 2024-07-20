import EncodeDecode
import sys
from typing import List, Tuple
from PIL import Image

def check_png(filename: str) -> None:
    try:
        with Image.open(filename) as img:
            if img.format != 'PNG':
                raise ValueError(f"The image file {filename} is not a PNG. Only PNG images are supported.")
    except IOError:
        raise ValueError(f"Unable to open the image file {filename}. Please ensure it's a valid PNG image.")

def bytes_to_bit_string(binary_data: bytes) -> str:
    # Convert a bytes object to a string of bits
    return ''.join(f'{byte:08b}' for byte in binary_data)

def bit_string_to_bytes(bit_string: str) -> bytes:
    # Convert a string of 1s and 0s to a bytes object.
    if not isinstance(bit_string, str):
        raise TypeError("Expected a string of 1s and 0s")
    if len(bit_string) % 8 != 0:
        raise ValueError("The bit string length must be a multiple of 8")
    return bytes(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

def file_to_binary(filename: str) -> bytes:
    # Convert a file to its binary representation.
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

def binary_to_file(binary_data: bytes, output_filename: str) -> None:
    # Write binary data to a file.
    with open(output_filename, 'wb') as file:
        file.write(binary_data)

def encode_file_in_image(file_name: str, image_filename: str) -> None:
    check_png(image_filename)
    print("Converting image to array")
    rgb_array_2d_int = EncodeDecode.convert_image_to_array(image_filename)

    print("Converting array to binary")
    rgb_array_2d_binary = EncodeDecode.convert_decimal_array_to_binary(rgb_array_2d_int)

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
    img_new.save(image_filename, format='PNG')

def decode_file_from_image(image_filename: str, output_filename: str) -> None:
    check_png(image_filename)
    print("Converting image to array")
    # Convert the image to an array of pixel values
    rgb_array_2d_decimal = EncodeDecode.convert_image_to_array(image_filename)
    print("Converting array to binary")
    rgb_array_2d_binary = EncodeDecode.convert_decimal_array_to_binary(rgb_array_2d_decimal)

    print("Extracting least significant bits")
    # Extract the least significant bits to get our encoded binary string
    decoded_bits = EncodeDecode.get_least_significant_bits_any(rgb_array_2d_binary)

    # Extract the original binary string length from the first 32 bits
    original_length = int(decoded_bits[:32], 2)

    # Trim the decoded_bits to only contain the original message
    decoded_bits = decoded_bits[32:32 + original_length]
    print("Constructing bytes from decoded bits")
    raw_bytes = bit_string_to_bytes(decoded_bits)
    print("Building file from bytes")
    binary_to_file(raw_bytes, output_filename)

def encode(file_in: str, image_out: str) -> None:
    encode_file_in_image(file_in, image_out)

def decode(image_in: str, file_out: str) -> None:
    decode_file_from_image(image_in, file_out)

if __name__ == "__main__":
    # command line arguments
    # encode into image:
    # python3 anyFile.py encode file_in image_out
    # decode out of image
    # python3 anyfile.py decode image_in file_out
    if len(sys.argv) != 4:
        raise ValueError("Incorrect number of arguments. Usage: python3 anyFile.py [encode|decode] input_file output_file")

    if sys.argv[1] not in ['encode', 'decode']:
        raise ValueError("First argument must be either 'encode' or 'decode'")

    if sys.argv[1] == 'encode':
        encode(file_in=sys.argv[2], image_out=sys.argv[3])
    elif sys.argv[1] == 'decode':
        decode(image_in=sys.argv[2], file_out=sys.argv[3])
