from django import forms

from .models import Page
from .watson import get_keywords


class PageForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Page
        fields = ['title']

    def save(self, commit=True):
        instance = super().save(commit=False)

        file = self.cleaned_data.get('file')

        # print(file.content_type)
        content = file.read().decode('utf-8')
        instance.content = content

        if commit:
            instance.save()

            # this has to be run after instance.save(), only if the file exists
            keywords = get_keywords(content)
            for keyword in keywords:
                instance.link_set.create(title=keyword['text'],
                                         relevance=keyword['relevance'])

        return instance
