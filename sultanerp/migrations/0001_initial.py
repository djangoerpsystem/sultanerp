# Generated by Django 3.0.3 on 2023-09-15 19:53

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('personal_nr', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CRMItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('inbox', 'Inbox'), ('in_progress', 'In Progress'), ('done', 'Done'), ('archive', 'Archive')], default='inbox', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('directory', models.CharField(max_length=255)),
                ('filesize_mb', models.FloatField(max_length=255)),
                ('creation_date', models.DateField()),
                ('file_url', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.TextField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternalProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posNr', models.CharField(blank=True, max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, choices=[('Teigwaren', 'Teigwaren'), ('Baklava', 'Baklava'), ('Konditorei', 'Konditorei'), ('Backstube', 'Backstube'), ('Snacks', 'Snacks'), ('Restaurant', 'Restaurant')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InventorySection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MeasureUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('unit_category', models.CharField(choices=[('weight', 'weight'), ('distance', 'distance'), ('packaging', 'packaging'), ('currency', 'currency')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('places', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicHoliday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Routines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routines', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoutinesCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoutineTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('frequency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sultanerp.Frequency')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sultanerp.Places')),
                ('routines', models.ManyToManyField(to='sultanerp.Routines')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branchTitle', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('categories', models.ManyToManyField(to='sultanerp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierOrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TortenBestellungsID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('cakePrice', models.FloatField(default=0.0)),
                ('quittung', models.IntegerField(null=True)),
                ('orderDate', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('field1', models.CharField(max_length=255)),
                ('field2', models.CharField(max_length=255)),
                ('field3', models.CharField(max_length=255)),
                ('field4', models.CharField(default='', max_length=255)),
                ('form_name', models.CharField(max_length=25)),
                ('status', models.CharField(default='Inbox', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VacationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_changed', models.DateTimeField(auto_now_add=True)),
                ('days_changed', models.IntegerField()),
                ('current_balance', models.PositiveIntegerField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacation_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VacationDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_added', models.PositiveIntegerField(default=24)),
                ('days_used', models.PositiveIntegerField(default=0)),
                ('works_day', models.PositiveIntegerField(blank=True, default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manual_vacation_days', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VacationApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('days_requested', models.PositiveIntegerField()),
                ('free_days', models.PositiveIntegerField(blank=True, null=True)),
                ('days_on_sunday', models.PositiveIntegerField(default=0)),
                ('days_on_holiday', models.PositiveIntegerField(default=0)),
                ('vacation_days', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('approval', models.CharField(blank=True, choices=[('no', 'no'), ('yes', 'yes')], max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Frequency')),
                ('routineTasks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.RoutineTasks')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('dueDate', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('open', 'open'), ('done', 'done')], default='open', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('responsiblePerson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SuppliersProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artNr', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('inhalt', models.CharField(blank=True, max_length=4, null=True)),
                ('suppliers', models.ManyToManyField(related_name='products', to='sultanerp.Supplier')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sultanerp.MeasureUnits')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productAmounts', models.CharField(blank=True, max_length=255, null=True)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField(default=None, null=True)),
                ('ordering_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(through='sultanerp.SupplierOrderProduct', to='sultanerp.SuppliersProduct')),
                ('store_branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Store')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sultanerp.Supplier')),
            ],
        ),
        migrations.AddField(
            model_name='supplierorderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.SupplierOrders'),
        ),
        migrations.AddField(
            model_name='supplierorderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.SuppliersProduct'),
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storagePlace', models.CharField(max_length=30)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Store')),
            ],
        ),
        migrations.AddField(
            model_name='routinetasks',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Store'),
        ),
        migrations.AddField(
            model_name='routinetasks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='routines',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.RoutinesCategory'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('log', models.TextField(max_length=20)),
                ('done', models.BooleanField(default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('loggedIn', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('boughtOn', models.DateField(blank=True, null=True)),
                ('value', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Category')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.InventorySection')),
                ('storedIn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Storage')),
            ],
        ),
        migrations.CreateModel(
            name='InternalOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderAmount', models.CharField(blank=True, max_length=255, null=True)),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('orderDate', models.DateField(default=datetime.date.today)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Store')),
                ('products', models.ManyToManyField(to='sultanerp.InternalProducts')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerName', models.CharField(max_length=255)),
                ('customerTel', models.CharField(max_length=50)),
                ('totalAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('orderDate', models.DateField(default=datetime.date.today)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sultanerp.Store')),
                ('products', models.ManyToManyField(to='sultanerp.InternalProducts')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='sultanerp.Store'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='sultanerp.Roles'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
