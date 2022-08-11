from django.db import models
from django.conf import settings

import textract

from .watson import get_keywords
from .docx import docx_parse


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_dir = models.CharField(max_length=150, null=True)
    url = models.CharField(max_length=150, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def build_from_file(self, fh):
        # We need a pk in order to save images from the document
        self.save()

        extension = fh.name.split('.')[-1]

        if extension == 'docx':
            image_dir = settings.MEDIA_ROOT / 'page_images' / str(self.pk)
            self.image_dir = image_dir

            content, content_raw = docx_parse(fh, image_dir)
        else:
            content = textract.process(fh.name).decode('utf-8')
            content_raw = content

        self.content = content
        self.save()

        keywords = get_keywords(content_raw)
        for keyword in keywords:
            self.link_set.create(title=keyword['text'],
                                 relevance=keyword['relevance'])


class Link(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    relevance = models.FloatField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', '-relevance']

    def __str__(self):
        return self.title
