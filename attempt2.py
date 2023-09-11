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



def convert_decimal_to_binary(decimal_in):
    binary_out = format(decimal_in, '08b')
    return binary_out


def convert_decimal_array_to_binary(image_array):
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            pixel[0] = convert_decimal_to_binary(pixel[0])
            pixel[1] = convert_decimal_to_binary(pixel[1])
            pixel[2] = convert_decimal_to_binary(pixel[2])
            image_array[i][j] = tuple(pixel)

    return image_array


def convert_string_to_binary_string(text):
    binary_string = ''
    for character in text:
        binary_string += format(ord(character), '08b')
    return binary_string


def adjust_least_significant_bit(image_array, binary_string):
    ##### ADD IN BOUNDS CHECK ON THE SIZE OF K #####
    k = 0
    pixel_count = 0
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



rgb_array_2d_decimal = convert_image_to_array('elon.jpeg')
rgb_array_2d_binary = convert_decimal_array_to_binary(rgb_array_2d_decimal)
print(rgb_array_2d_binary)

binary_string = convert_string_to_binary_string('Hello, world!')
print(binary_string)

rgb_array_2d_binary = adjust_least_significant_bit(rgb_array_2d_binary, binary_string)
print(rgb_array_2d_binary)
