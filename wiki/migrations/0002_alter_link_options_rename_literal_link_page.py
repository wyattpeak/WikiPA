# Generated by Django 4.0.5 on 2022-06-09 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['page', '-relevance']},
        ),
        migrations.RenameField(
            model_name='link',
            old_name='literal',
            new_name='page',
        ),
    ]
