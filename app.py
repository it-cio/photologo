import os

from PIL import Image


def insert_logo(input_photo_path, output_photo_path, logo_path):
    base_image = Image.open(input_photo_path)
    logo = Image.open(logo_path)
    width, height = base_image.size

    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))

    fixed_width = int(base_image.width / 100 * 15)
    width_percent = fixed_width / logo.width * 100
    height_size = int(logo.height / 100 * width_percent)
    logo_resize = logo.resize((fixed_width, height_size))
    indent = int(base_image.height / 100 * 5)
    position = (base_image.width - (logo_resize.width + indent),
                base_image.height - (logo_resize.height + indent))
    transparent.paste(logo_resize, position, mask=logo_resize)
    # transparent.show()
    transparent.save(output_photo_path)


if __name__ == '__main__':
    for file in os.listdir():
        if file.lower().endswith('.jpg'):
            if not os.path.isdir('modified'):
                os.mkdir('modified')
            insert_logo(file, f'modified/logo_{file}', 'logo/logo.png')
