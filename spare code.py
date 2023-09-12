for y in range(height):
    row = []
    for x in range(width):
        # Get RGB values of each pixel
        r, g, b = img.getpixel((x, y))

        # Append the RGB tuple to the row
        row.append((r, g, b))

    # Append the row to the 2D array
    rgb_array_2d.append(row)


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
                    k += 1

                if not pixel[1].endswith(binary_string[k]):
                    red = pixel[0]
                    red = list(red)
                    red[len(red) - 1] = binary_string[k]
                    pixel[0] = ''.join(red)
                    k += 1

                if not pixel[2].endswith(binary_string[k]):
                    red = pixel[0]
                    red = list(red)
                    red[len(red) - 1] = binary_string[k]
                    pixel[0] = ''.join(red)
                    k += 1

                image_array[i][j] = tuple(pixel)

        return image_array