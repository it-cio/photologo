import os

from PIL import Image


def insert_logo(input_photo_path, output_photo_path, logo_path, position):
    base_image = Image.open(input_photo_path)
    logo = Image.open(logo_path)
    width, height = base_image.size

    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(logo, position, mask=logo)
    # transparent.show()
    transparent.save(output_photo_path)


if __name__ == '__main__':
    for file in os.listdir():
        if file.lower().endswith('.jpg'):
            insert_logo(file, f'logo/logo_{file}',
                        'logo/logo.png', position=(0, 50))
