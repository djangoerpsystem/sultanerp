# Generated by Django 3.0.3 on 2023-09-16 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sultanerp', '0010_auto_20230916_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customerorders',
            name='delivery_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Delivery'),
        ),
    ]