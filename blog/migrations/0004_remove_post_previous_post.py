# Generated by Django 2.2.7 on 2019-11-26 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191126_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='previous_post',
        ),
    ]
