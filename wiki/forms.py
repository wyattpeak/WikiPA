from django import forms

from .models import Page
from .watson import get_keywords

from tempfile import NamedTemporaryFile
import textract


class PageForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Page
        fields = ['title']

    def save(self, commit=True):
        instance = super().save(commit=False)

        file = self.cleaned_data.get('file')

        extension = file.name.split('.')[-1]
        with NamedTemporaryFile(mode='w+b', suffix=f'.{extension}') as fh:
            fh.write(file.read())
            fh.seek(0)

            content = textract.process(fh.name).decode('utf-8')
            instance.content = content

        if commit:
            instance.save()

            # this has to be run after instance.save(), only if the file exists
            keywords = get_keywords(content)
            for keyword in keywords:
                instance.link_set.create(title=keyword['text'],
                                         relevance=keyword['relevance'])

        return instance
