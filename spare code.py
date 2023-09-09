for y in range(height):
    row = []
    for x in range(width):
        # Get RGB values of each pixel
        r, g, b = img.getpixel((x, y))

        # Append the RGB tuple to the row
        row.append((r, g, b))

    # Append the row to the 2D array
    rgb_array_2d.append(row)