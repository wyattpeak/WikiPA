from django import forms
from django.core.exceptions import ValidationError

from .models import Page, Category
from .backup import load

from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import tarfile


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
                    title = title.split('/')[-1]

                    with NamedTemporaryFile(mode='w+b', suffix=f'.{extension}') as fh:
                        fh.write(docfile.read())
                        fh.seek(0)

                        page = Page(title=title)
                        page.build_from_file(fh)
                        page.save()


class BackupLoadForm(forms.Form):
    file = forms.FileField(label='Archive file')

    class Meta:
        model = Page
        fields = ['title']

    def clean(self):
        file = self.cleaned_data.get("file")
        extension = file.name.split('.')[-1]
        if extension != 'tgz':
            self.add_error('file', ValidationError('The archive import function only supports tgz files.'))

        return self.cleaned_data

    def save(self, commit=True):
        if not commit:
            raise ValueError('Saving this form without committing is not implemented.')

        file = self.cleaned_data.get('file')
        with tarfile.open(fileobj=file, mode='r:gz') as tar:
            load(tar)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    # def save(self, commit=True):
    #     instance = super().save(commit=False)

    #     file = self.cleaned_data.get('file')

    #     extension = file.name.split('.')[-1]
    #     with NamedTemporaryFile(mode='w+b', suffix=f'.{extension}') as fh:
    #         fh.write(file.read())
    #         fh.seek(0)

    #         instance.build_from_file(fh)

    #     return instance
