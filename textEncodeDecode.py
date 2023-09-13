import time

import EncodeDecode


def convert_string_to_binary_string(text):
    binary_string = ''
    for character in text:
        binary_string += format(ord(character), '08b')
    binary_string += '11111111'  # Termination sequence
    return binary_string


def decode_text_from_image(image_filename):
    # Convert the image to an array of pixel values
    rgb_array_2d_decimal = EncodeDecode.convert_image_to_array(image_filename)
    rgb_array_2d_binary = EncodeDecode.convert_decimal_array_to_binary(rgb_array_2d_decimal)

    # Extract the least significant bits to get our encoded binary string
    decoded_bits = EncodeDecode.get_least_significant_bits_text(rgb_array_2d_binary)

    # Group bits by 8 to create bytes
    binary_strings = [''.join(decoded_bits[i:i + 8]) for i in range(0, len(decoded_bits), 8)]

    decoded_text = []
    for binary_string in binary_strings:
        if binary_string == '11111111':  # termination sequence
            break
        char = chr(int(binary_string, 2))
        decoded_text.append(char)

    return ''.join(decoded_text)


def encode_text_in_image(text, image_filename):
    rgb_array_2d_decimal = EncodeDecode.convert_image_to_array(image_filename)
    rgb_array_2d_binary = EncodeDecode.convert_decimal_array_to_binary(rgb_array_2d_decimal)
    print(rgb_array_2d_binary)

    binary_string = convert_string_to_binary_string(text)
    print(binary_string)
    time.sleep(1)

    rgb_array_2d_binary = EncodeDecode.adjust_least_significant_bit(rgb_array_2d_binary, binary_string)
    print(rgb_array_2d_binary)

    # convert image back to decimal array
    rgb_array_2d_decimal = EncodeDecode.convert_binary_array_to_decimal(rgb_array_2d_binary)
    # print(rgb_array_2d_decimal)

    # convert decimal array to image
    img_new = EncodeDecode.convert_array_to_image(rgb_array_2d_decimal)
    img_new.save('test.png')


# Open the file for reading

with open('hamlet.txt', 'r') as file:
    content = file.read()

encode_text_in_image(content, 'elon.jpeg')
decoded_text = decode_text_from_image('test.png')
print(decoded_text)
