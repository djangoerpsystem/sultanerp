# Generated by Django 3.0.3 on 2023-09-16 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0007_customerorders_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEntries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termin', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
