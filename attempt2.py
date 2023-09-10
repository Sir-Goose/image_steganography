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

def adjust_least_significant_bit(image_array, binary_string):
    ##### ADD IN BOUNDS CHECK ON THE SIZE OF K #####
    k = 0
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            if not pixel[0].endswith(binary_string[k]):
                pixel[0][len(pixel) - 1] = binary_string[k]
                k += 1

            if not pixel[1].endswith(binary_string[k]):
                pixel[1][len(pixel) - 1] = binary_string[k]
                k += 1

            if not pixel[2].endswith(binary_string[k]):
                pixel[2][len(pixel) - 1] = binary_string[k]
                k += 1

            image_array[i][j] = tuple(pixel)

    return image_array



rgb_array_2d_decimal = convert_image_to_array('elon.jpeg')
rgb_array_2d_binary = convert_decimal_array_to_binary(rgb_array_2d_decimal)


print(rgb_array_2d_binary)
