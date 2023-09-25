# Generated by Django 3.0.3 on 2023-09-16 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0009_auto_20230916_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarentriesoffice',
            name='user_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Roles'),
        ),
        migrations.AddField(
            model_name='calendarentriesstore',
            name='user_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Roles'),
        ),
    ]