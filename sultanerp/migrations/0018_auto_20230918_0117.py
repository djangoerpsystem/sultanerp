# Generated by Django 3.0.3 on 2023-09-17 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0017_message_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]