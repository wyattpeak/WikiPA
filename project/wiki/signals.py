from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Page
from .mediawiki import delete_from_wiki


@receiver(pre_delete, sender=Page)
def delete_page(sender, instance, **kwargs):
    if instance.url:
        delete_from_wiki(instance)
