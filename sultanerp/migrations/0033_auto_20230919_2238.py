# Generated by Django 3.0.3 on 2023-09-19 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0032_auto_20230919_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('customer', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='wiki',
            name='header',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
