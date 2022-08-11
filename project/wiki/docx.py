import os
import shutil
import mammoth
import re


class ImageWriter(object):
    def __init__(self, output_dir):
        self._output_dir = output_dir
        self._image_number = 1

    def __call__(self, element):
        extension = element.content_type.partition('/')[2]
        image_filename = f'{self._image_number}.{extension}'
        image_path = os.path.join(self._output_dir, image_filename)
        with open(image_path, 'wb') as fh:
            with element.open() as img:
                shutil.copyfileobj(img, fh)

        self._image_number += 1

        return {'src': image_filename}


def docx_parse(fh, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    convert_image = mammoth.images.inline(ImageWriter(output_dir))

    result = mammoth.convert_to_html(fh, convert_image=convert_image)
    content = result.value

    # Remove links without href attribute from content, don't know why they're inserted
    content = re.sub(r'<a[^>]*(?!href="[^"]*")[^>]>.*?</a>', '', content)

    # Give borders to tables
    content = content.replace('<table>', '<table class="wikitable">')

    result_raw = mammoth.extract_raw_text(fh)
    content_raw = result_raw.value

    return content, content_raw
