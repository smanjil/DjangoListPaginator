# Generated by Django 2.0 on 2017-12-09 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genericviews', '0003_auto_20171209_0251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user_id',
            new_name='user',
        ),
    ]
