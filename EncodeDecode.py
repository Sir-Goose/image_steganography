import time

from PIL import Image


def convert_image_to_array(image_in):
    # Open the image using PIL
    img = Image.open(image_in)

    # Convert image to RGB (in case it's in another format like RGBA or Grayscale)
    img = img.convert("RGB")

    # Get image dimensions
    width, height = img.size

    # Create a 2D array to store the RGB values of each pixel
    rgb_array_2d = []

    # Loop through each row
    for y in range(height):
        row = []
        for x in range(width):
            # Get RGB values of each pixel
            r, g, b = img.getpixel((x, y))

            # Append the RGB tuple to the row
            row.append((r, g, b))

        # Append the row to the 2D array
        rgb_array_2d.append(row)

    return rgb_array_2d


def convert_array_to_image(rgb_array_2d):
    # Determine the dimensions of the 2D array
    height = len(rgb_array_2d)
    width = len(rgb_array_2d[0])

    # Create a new blank image with the same dimensions
    img_new = Image.new("RGB", (width, height))

    # Populate the new image with the RGB values from the 2D array
    for y in range(height):
        for x in range(width):
            # Get the RGB values from the 2D array
            r, g, b = rgb_array_2d[y][x]

            # Set the RGB values for each pixel in the new image
            img_new.putpixel((x, y), (r, g, b))

    return img_new


def convert_decimal_to_binary(decimal_in):
    binary_out = format(decimal_in, '08b')
    return binary_out


def convert_binary_to_decimal(binary_in):
    decimal_out = int(binary_in, 2)
    return decimal_out


def convert_decimal_array_to_binary(image_array):
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            pixel[0] = convert_decimal_to_binary(pixel[0])
            pixel[1] = convert_decimal_to_binary(pixel[1])
            pixel[2] = convert_decimal_to_binary(pixel[2])
            image_array[i][j] = tuple(pixel)

    return image_array


def convert_binary_array_to_decimal(image_array):
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            pixel[0] = convert_binary_to_decimal(pixel[0])
            pixel[1] = convert_binary_to_decimal(pixel[1])
            pixel[2] = convert_binary_to_decimal(pixel[2])
            image_array[i][j] = tuple(pixel)

    return image_array


def convert_string_to_binary_string(text):
    binary_string = ''
    for character in text:
        binary_string += format(ord(character), '08b')
    binary_string += '11111111'  # Termination sequence
    return binary_string


def adjust_least_significant_bit(image_array, binary_string):
    k = 0
    pixel_count = 0

    if len(binary_string) > len(image_array) * len(image_array[0]) * 3:  # 3 for RGB
        raise ValueError("Message is too long to be encoded in this image!")

    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            if k >= len(binary_string):  # Exit if we've embedded all bits
                return image_array

            pixel = list(image_array[i][j])

            # Adjusting the LSB for the red channel
            red = list(pixel[0])
            red[-1] = binary_string[k]
            pixel[0] = ''.join(red)
            k += 1

            if k >= len(binary_string):  # Check again after every channel
                return image_array

            # Adjusting the LSB for the green channel
            green = list(pixel[1])
            green[-1] = binary_string[k]
            pixel[1] = ''.join(green)
            k += 1

            if k >= len(binary_string):  # And again
                return image_array

            # Adjusting the LSB for the blue channel
            blue = list(pixel[2])
            blue[-1] = binary_string[k]
            pixel[2] = ''.join(blue)
            k += 1

            image_array[i][j] = tuple(pixel)

    return image_array


def get_least_significant_bits(image_array):
    decoded_bits = []
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            decoded_bits.append(pixel[0][len(pixel[0]) - 1])
            decoded_bits.append(pixel[1][len(pixel[1]) - 1])
            decoded_bits.append(pixel[2][len(pixel[2]) - 1])
    return decoded_bits


def convert_8_bit_binary_to_character(binary_string):
    character = chr(int(binary_string, 2))
    return character


def encode_text_in_image():
    rgb_array_2d_decimal = convert_image_to_array('elon.jpeg')
    rgb_array_2d_binary = convert_decimal_array_to_binary(rgb_array_2d_decimal)
    print(rgb_array_2d_binary)

    # Open the file for reading
    with open('hamlet.txt', 'r') as file:
        content = file.read()

    # print(content)  # This will print the contents of the file
    # time.sleep(1)

    binary_string = convert_string_to_binary_string(content)
    print(binary_string)
    time.sleep(1)

    rgb_array_2d_binary = adjust_least_significant_bit(rgb_array_2d_binary, binary_string)
    print(rgb_array_2d_binary)

    # convert image back to decimal array
    rgb_array_2d_decimal = convert_binary_array_to_decimal(rgb_array_2d_binary)
    # print(rgb_array_2d_decimal)

    # convert decimal array to image
    img_new = convert_array_to_image(rgb_array_2d_decimal)
    img_new.save('test.png')


def decode_text_from_image(image_filename):
    # Convert the image to an array of pixel values
    rgb_array_2d_decimal = convert_image_to_array(image_filename)
    rgb_array_2d_binary = convert_decimal_array_to_binary(rgb_array_2d_decimal)

    # Extract the least significant bits to get our encoded binary string
    decoded_bits = get_least_significant_bits(rgb_array_2d_binary)

    # Group bits by 8 to create bytes
    binary_strings = [''.join(decoded_bits[i:i + 8]) for i in range(0, len(decoded_bits), 8)]

    decoded_text = []
    for binary_string in binary_strings:
        if binary_string == '11111111':  # termination sequence
            break
        char = chr(int(binary_string, 2))
        decoded_text.append(char)

    return ''.join(decoded_text)


encode_text_in_image()
decoded_text = decode_text_from_image('test.png')
print(decoded_text)
