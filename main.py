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


if __name__ == '__main__':
    text = 'Hello, world!'
    binary = convert_text_to_binary(text)

    for character in binary:
        print(character)
    print(binary)

    print(check_sufficient_capacity('elon.jpeg', text))
