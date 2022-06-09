from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Link(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    relevance = models.FloatField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', '-relevance']

    def __str__(self):
        return self.title