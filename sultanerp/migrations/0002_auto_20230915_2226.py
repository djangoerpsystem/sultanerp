# Generated by Django 3.0.3 on 2023-09-15 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorders',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]