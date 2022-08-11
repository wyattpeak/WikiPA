from django import forms
from django.core.exceptions import ValidationError

from tempfile import NamedTemporaryFile
from zipfile import ZipFile

from .models import Page


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

            instance.build_from_file(fh)

        return instance


class PageBulkImportForm(forms.Form):
    file = forms.FileField(label='Zip file')

    def clean(self):
        file = self.cleaned_data.get("file")
        extension = file.name.split('.')[-1]
        if extension != 'zip':
            self.add_error('file', ValidationError('The bulk import function only supports zip files.'))

        return self.cleaned_data

    def save(self, commit=True):
        if not commit:
            raise ValueError('Saving this form without committing is not implemented.')

        file = self.cleaned_data.get('file')
        with ZipFile(file) as zipfile:
            for doc_filename in zipfile.namelist():
                with zipfile.open(doc_filename) as docfile:
                    title, extension = docfile.name.rsplit('.')

                    with NamedTemporaryFile(mode='w+b', suffix=f'.{extension}') as fh:
                        fh.write(docfile.read())
                        fh.seek(0)

                        page = Page(title=title)
                        page.build_from_file(fh)
                        page.save()
