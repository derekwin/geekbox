# Generated by Django 3.0.6 on 2020-06-02 09:33

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geek_library', '0008_auto_20200527_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=ckeditor.fields.RichTextField(blank=True, help_text='丛书简介：', null=True, verbose_name='简述'),
        ),
    ]
