# Generated by Django 3.0.6 on 2020-06-23 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200620_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='documents',
            field=models.FileField(default=12, max_length=200, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='documents',
            field=models.FileField(default=12, max_length=200, upload_to='media'),
            preserve_default=False,
        ),
    ]
