# Generated by Django 3.0.3 on 2023-09-17 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0016_retoure'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
