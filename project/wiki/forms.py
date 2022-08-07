from django import forms
from django.conf import settings

from tempfile import NamedTemporaryFile
import textract
import os

from .models import Page
from .watson import get_keywords
from .docx import docx_parse


class PageForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Page
        fields = ['title']

    def save(self, commit=True):
        if not commit:
            raise ValueError('Saving this form without committing is not implemented.')

        instance = super().save(commit=False)
        instance.save()

        file = self.cleaned_data.get('file')

        extension = file.name.split('.')[-1]
        with NamedTemporaryFile(mode='w+b', suffix=f'.{extension}') as fh:
            fh.write(file.read())
            fh.seek(0)

            if extension == 'docx':
                image_dir = settings.MEDIA_ROOT / 'page_images' / str(instance.pk)
                instance.image_dir = image_dir

                content, content_raw = docx_parse(fh, image_dir)
            else:
                content = textract.process(fh.name).decode('utf-8')
                content_raw = content

            instance.content = content

        instance.save()

        # this has to be run after instance.save(), only if the file exists
        keywords = get_keywords(content_raw)
        for keyword in keywords:
            instance.link_set.create(title=keyword['text'],
                                     relevance=keyword['relevance'])

        return instance
