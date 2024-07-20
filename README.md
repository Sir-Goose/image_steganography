# Image Steganography Tool

This Python script allows you to encode any file into a PNG image and decode it back, using steganography techniques. The tool modifies the least significant bits of the image's pixel values to store the data, making the changes imperceptible to the human eye.

## Requirements

- Python 3.x
- Pillow (PIL) library

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies:
   ```
   pip3 install Pillow
   ```

## Usage

### Encoding data into an image:

```
python3 anyFile.py encode <input_file> <output_image.png>
```

Example:
```
python3 anyFile.py encode hamlet.txt cat.png
```

This will encode the contents of `hamlet.txt` into `cat.png`. The resulting image will look identical to the original to the human eye.

### Decoding data from an image:

```
python3 anyFile.py decode <input_image.png> <output_file>
```

Example:
```
python3 anyFile.py decode cat.png message.txt
```

This will extract the hidden data from `cat.png` and save it to `message.txt`.

## How It Works

1. The script converts the input file to binary data.
2. It then modifies the least significant bit of each color channel in each pixel of the PNG image to store this binary data.
3. When decoding, it reads these least significant bits to reconstruct the original file.

## Limitations

- Only PNG images are supported due to their lossless compression (BMP and other lossless formats may work).
- The size of the data you can hide is limited to about 3 bits per pixel.

## Screenshots

### Encoding Process
<img width="1072" alt="Encoding Process" src="https://github.com/user-attachments/assets/4c454eeb-899e-46df-9a22-c4373a551c66">

### Decoding Process
<img width="1840" alt="Decoding Process" src="https://github.com/user-attachments/assets/346a3115-c48b-48db-8c03-29de27fe492f">

## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes.

