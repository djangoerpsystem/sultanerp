# Generated by Django 3.0.3 on 2023-09-19 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0025_auto_20230919_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('user_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
