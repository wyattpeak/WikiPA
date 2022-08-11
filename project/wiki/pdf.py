import os
from pdf2image import convert_from_bytes


def pdf_parse_as_images(fh, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_bytes = fh.read()
    pages = convert_from_bytes(file_bytes)

    content = ''

    for index, page in enumerate(pages):
        image_filename = f'{index}.png'
        image_path = os.path.join(output_dir, image_filename)

        page.save(image_path, 'PNG')

        content += f'<p><img src="{image_filename}" /></p>'

    return content, ''
