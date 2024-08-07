from PIL import Image
from typing import List, Tuple

def convert_image_to_array(image_in: str) -> List[List[Tuple[int, int, int]]]:
    # Open the image using PIL
    img = Image.open(image_in)

    # Convert image to RGB (in case it's in another format like RGBA or Grayscale)
    img = img.convert("RGB")

    # Get image dimensions
    width, height = img.size

    # Create a 2D array to store the RGB values of each pixel
    rgb_array_2d: List[List[Tuple[int, int, int]]] = []

    # Loop through each row
    for y in range(height):
        row: List[Tuple[int, int, int]] = []
        for x in range(width):
            # Get RGB values of each pixel
            r, g, b = img.getpixel((x, y))

            # Append the RGB tuple to the row
            row.append((r, g, b))

        # Append the row to the 2D array
        rgb_array_2d.append(row)

    return rgb_array_2d

def convert_array_to_image(rgb_array_2d: List[List[Tuple[int, int, int]]]) -> Image.Image:
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

def convert_int_to_binary(int_in: int) -> str:
    binary_out = format(int_in, '08b')
    return binary_out

def convert_binary_to_decimal(binary_in: str) -> int:
    decimal_out = int(binary_in, 2)
    return decimal_out

def convert_decimal_array_to_binary(image_array: List[List[Tuple[int, int, int]]]) -> List[List[Tuple[str, str, str]]]:
    result: List[List[Tuple[str, str, str]]] = []
    for row in image_array:
        new_row: List[Tuple[str, str, str]] = []
        for pixel in row:
            r, g, b = pixel
            new_pixel = (
                convert_int_to_binary(r),
                convert_int_to_binary(g),
                convert_int_to_binary(b)
            )
            new_row.append(new_pixel)
        result.append(new_row)
    return result

def convert_binary_array_to_decimal(image_array: List[List[Tuple[str, str, str]]]) -> List[List[Tuple[int, int, int]]]:
    result: List[List[Tuple[int, int, int]]] = []
    for row in image_array:
        new_row: List[Tuple[int, int, int]] = []
        for pixel in row:
            r, g, b = pixel
            new_pixel = (
                convert_binary_to_decimal(r),
                convert_binary_to_decimal(g),
                convert_binary_to_decimal(b)
            )
            new_row.append(new_pixel)
        result.append(new_row)
    return result

def adjust_least_significant_bit(image_array: List[List[Tuple[str, str, str]]], binary_string: str) -> List[List[Tuple[str, str, str]]]:
    k = 0
    pixel_count = 0

    if len(binary_string) > len(image_array) * len(image_array[0]) * 3:  # 3 for RGB
        raise ValueError("File is too big to be encoded in this image!")

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

def get_least_significant_bits_text(image_array: List[List[Tuple[str, str, str]]]) -> List[str]:
    decoded_bits = []
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            decoded_bits.append(pixel[0][len(pixel[0]) - 1])
            decoded_bits.append(pixel[1][len(pixel[1]) - 1])
            decoded_bits.append(pixel[2][len(pixel[2]) - 1])
    return decoded_bits

def get_least_significant_bits_any(image_array: List[List[Tuple[str, str, str]]]) -> str:
    decoded_bits = []
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            pixel = list(image_array[i][j])
            decoded_bits.append(pixel[0][len(pixel[0]) - 1])
            decoded_bits.append(pixel[1][len(pixel[1]) - 1])
            decoded_bits.append(pixel[2][len(pixel[2]) - 1])
    return ''.join(decoded_bits)  # Convert the list to a string
