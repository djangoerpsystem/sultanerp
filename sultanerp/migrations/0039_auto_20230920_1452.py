# Generated by Django 3.0.3 on 2023-09-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0038_auto_20230920_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorders',
            name='orderDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
