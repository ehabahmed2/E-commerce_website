# Generated by Django 5.1 on 2024-09-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default='Categories/description', max_length=200),
        ),
    ]
