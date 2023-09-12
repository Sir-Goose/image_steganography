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
            pixel = list(image_array[i][j])
            print("K is: ")
            print(k)
            print("pixel count is: ")
            print(pixel_count)
            pixel_count += 1

            if not pixel[0].endswith(binary_string[k]):
                red = pixel[0]
                red = list(red)
                red[len(red) - 1] = binary_string[k]
                pixel[0] = ''.join(red)
                if k < (len(binary_string) - 1):
                    k += 1

            if not pixel[1].endswith(binary_string[k]):
                green = pixel[1]
                green = list(green)
                green[len(green) - 1] = binary_string[k]
                pixel[1] = ''.join(green)
                if k < (len(binary_string) - 1):
                    k += 1

            if not pixel[2].endswith(binary_string[k]):
                blue = pixel[2]
                blue = list(blue)
                blue[len(blue) - 1] = binary_string[k]
                pixel[2] = ''.join(blue)
                if k < (len(binary_string) - 1):
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

    print(content)  # This will print the contents of the file
    time.sleep(1)

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


def decode_text_from_image():
    print("decoding...")
    rgb_array_2d_decimal = convert_image_to_array('test.png')
    rgb_array_2d_binary = convert_decimal_array_to_binary(rgb_array_2d_decimal)
    decoded_bits = get_least_significant_bits(rgb_array_2d_binary)

    binary_characters = []
    character = []
    for bit in decoded_bits:
        character.append(bit)
        if len(character) == 8:  # if we have 8 bits
            binary_characters.append(character)  # append the 8-bit character to the list
            character = []  # reset for the next character

    decoded_message = []
    for char_bin in binary_characters:
        if char_bin == '11111111':  # Termination sequence
            break
        decoded_message.append(convert_8_bit_binary_to_character(''.join(char_bin)))

    # If there are leftover bits that didn't form a full 8-bit character
    if character:
        binary_characters.append(character)

    text_characters = []
    print(binary_characters)

    # print(text_characters)

    for character in binary_characters:
        text_characters.append(convert_8_bit_binary_to_character(''.join(character)))

    print(text_characters)

    with open('decoded.txt', 'w') as file:
        file.write(''.join(text_characters))

    # read LSB of each color value of each pixel and add to array of arrays of 8 bits each
    # one array of 8 bits for each character


# encode_text_in_image()
# decode_text_from_image()

print(convert_8_bit_binary_to_character('0110100001100111'))