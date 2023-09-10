from PIL import Image


def convert_text_to_binary(text_in):
    binary_out = []
    for character in text_in:
        binary_out.append(format(ord(character), '08b'))
    return binary_out


def convert_binary_to_text(binary_in):
    text_out = ''
    for character in binary_in:
        text_out += chr(int(character, 2))
    return text_out


def binaray_addition(binary_in):
    return


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

def check_sufficient_capacity(image_in, text_in):
    # Open the image using PIL
    img = Image.open(image_in)

    # Convert image to RGB (in case it's in another format like RGBA or Grayscale)
    img = img.convert("RGB")

    # Get image dimensions
    width, height = img.size

    image_capacity = width * height * 3
    binary = convert_text_to_binary(text_in)
    binary_size = len(binary) * 8

    return image_capacity >= binary_size


def encode_text_in_image(image_array_in, text_in):
    if check_sufficient_capacity(image_array_in, text_in):
        print('Sufficient capacity')
    else:
        print('Insufficient capacity')
        return

    bit_array = []
    binary_text = convert_text_to_binary(text_in)
    for character in binary_text:
        for bit in character:
            bit_array.append(bit)

    i = 0
    for row in image_array_in:
        for pixel in row:
            for color in pixel:
                print(color)



    return



if __name__ == '__main__':
    text = 'Hello, world!'
    binary = convert_text_to_binary(text)

    for character in binary:
        print(character)
    print(binary)

    print(check_sufficient_capacity('elon.jpeg', text))
    encode_text_in_image(convert_image_to_array('elon.jpeg'), text)



