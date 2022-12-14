# Generated by Django 4.0.5 on 2022-08-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_page_image_dir'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='categories',
            field=models.ManyToManyField(to='wiki.category'),
        ),
    ]
