# Generated by Django 3.0.3 on 2023-09-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0008_calendarentries'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEntriesOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termin', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('label', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarEntriesStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termin', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('label', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CalendarEntries',
        ),
    ]