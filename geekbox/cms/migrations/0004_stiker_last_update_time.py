# Generated by Django 3.0.6 on 2020-05-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20200528_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='stiker',
            name='last_update_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]