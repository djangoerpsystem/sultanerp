# Generated by Django 3.0.3 on 2023-09-16 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0014_auto_20230916_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplierorders',
            old_name='store_branch',
            new_name='branch',
        ),
    ]
