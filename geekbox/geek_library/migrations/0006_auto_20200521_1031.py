# Generated by Django 3.0.6 on 2020-05-21 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geek_library', '0005_auto_20200520_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='data_birth',
            field=models.DateField(blank=True, null=True, verbose_name='出生于'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=100, verbose_name='名字'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, help_text='书籍ISBN编号', max_length=13, null=True, verbose_name='ISBN编号'),
        ),
        migrations.AlterField(
            model_name='book',
            name='stars',
            field=models.IntegerField(blank=True, help_text='喜欢人数', null=True, verbose_name='stars'),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(blank=True, help_text='丛书简介：', max_length=1000, null=True, verbose_name='简述'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='输入书籍的类型(比如，python，linux，技术，非技术等等)', max_length=200, verbose_name='类别名字'),
        ),
    ]