from django.core.management import call_command
from django.conf import settings

from .models import Page

import tempfile
import tarfile
import io
import os
import shutil
import re


def dump_add_dbdata(tar):
    dbdata_textIO = io.TextIOWrapper(io.BytesIO(), encoding='utf8')
    call_command('dumpdata', 'wiki', stdout=dbdata_textIO)
    dbdata_bytesIO = dbdata_textIO.detach()

    dbdata_tarinfo = tarfile.TarInfo(name='dump.json')
    dbdata_tarinfo.size = dbdata_bytesIO.tell()

    dbdata_bytesIO.seek(0)
    tar.addfile(tarinfo=dbdata_tarinfo, fileobj=dbdata_bytesIO)
    dbdata_bytesIO.close()


def dump_add_media(tar):
    for page in Page.objects.all():
        page_img_dir = settings.MEDIA_ROOT / 'page_images' / str(page.pk)
        page_arc_dir = f'media/page_images/{page.pk}'
        tar.add(page_img_dir, page_arc_dir)


def dump():
    with tempfile.TemporaryFile(mode='r+b', suffix='.tgz') as fh:
        with tarfile.open(fileobj=fh, mode='w:gz') as tar:
            dump_add_dbdata(tar)
            dump_add_media(tar)

        fh.seek(0)
        return fh.read()


def load(tar):
    if Page.objects.count() != 0:
        raise ValueError('Cannot load a backup when pages already exist.')

    page_images_dir = settings.MEDIA_ROOT / 'page_images'
    if os.path.exists(page_images_dir):
        shutil.rmtree(page_images_dir)

    # matches valid files and directories, avoid malicious uploads
    file_pattern = re.compile(r'^media/page_images/\d+(/\d+\.(jpe?g|png|gif))?$')

    for item in tar.getmembers():
        if file_pattern.match(item.name):
            tar.extract(item, settings.BASE_DIR)

        if item.name == 'dump.json':
            with tempfile.TemporaryDirectory() as tempdir:
                tar.extract(item, tempdir)
                filepath = os.path.join(tempdir, 'dump.json')
                call_command('loaddata', filepath)
