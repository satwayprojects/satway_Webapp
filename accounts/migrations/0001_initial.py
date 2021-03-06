# Generated by Django 3.2.4 on 2021-07-29 15:13

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('US', 'User'), ('SU', 'Subuser'), ('DI', 'Distributer'), ('DE', 'Dealer'), ('SD', 'Subdealer'), ('AD', 'Admin')], default='AD', max_length=2)),
                ('first_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(help_text='Phone number without Country Code', max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('added_by', models.CharField(max_length=50)),
                ('company_details', models.CharField(blank=True, max_length=150, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='deviceTable',
            fields=[
                ('imei', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('icc_id', models.CharField(max_length=30, unique=True)),
                ('unique_id', models.CharField(max_length=30, unique=True)),
                ('primary_contact', models.DecimalField(decimal_places=0, max_digits=13, unique=True)),
                ('secondary_contact', models.DecimalField(decimal_places=0, max_digits=13, unique=True)),
                ('version', models.CharField(max_length=20)),
                ('activation_status', models.BooleanField()),
                ('activation_date', models.DateField(blank=True, null=True)),
                ('added_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('current_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'deviceTable',
            },
        ),
        migrations.CreateModel(
            name='vehicleDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_no', models.CharField(blank=True, max_length=30, unique=True)),
                ('installation_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('handled_by', models.CharField(blank=True, max_length=50, null=True)),
                ('odometer', models.BigIntegerField(blank=True, default=0, help_text='Distance travelled by the vehicle')),
                ('imei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.devicetable')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'vehicleDetails',
            },
        ),
        migrations.CreateModel(
            name='user_vehicle_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renewal_of_data', models.DateField(blank=True, null=True)),
                ('renewal_of_insurance', models.DateField(blank=True, null=True)),
                ('renewal_of_fitness', models.DateField(blank=True, null=True)),
                ('renewal_of_pollution', models.DateField(blank=True, null=True)),
                ('renewal_of_tax', models.DateField(blank=True, null=True)),
                ('driver_mobile', models.CharField(blank=True, help_text='Phone number without Country Code', max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('vehicle_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.vehicledetails', to_field='vehicle_no')),
            ],
            options={
                'db_table': 'user_vehicle_services',
            },
        ),
        migrations.CreateModel(
            name='transactionTable',
            fields=[
                ('held_by', models.CharField(max_length=50)),
                ('imei_held_by', models.CharField(default='imei+held_by', max_length=100, primary_key=True, serialize=False)),
                ('transaction_date', models.DateField(default=datetime.datetime.now, null=True)),
                ('last_transaction', models.BooleanField()),
                ('imei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.devicetable')),
                ('sold_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'transactionTable',
            },
        ),
        migrations.CreateModel(
            name='live_location_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('speed', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ignition', models.IntegerField(blank=True, null=True)),
                ('vehicle_mode', models.CharField(blank=True, max_length=1, null=True)),
                ('power_status', models.IntegerField(blank=True, null=True)),
                ('alert_data', models.IntegerField(blank=True, null=True)),
                ('imei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.devicetable')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'live_location_table',
            },
        ),
        migrations.CreateModel(
            name='device_data_database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField()),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('speed', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ignition', models.IntegerField(blank=True, null=True)),
                ('vehicle_mode', models.CharField(blank=True, max_length=1, null=True)),
                ('power_status', models.IntegerField(null=True)),
                ('alert_data', models.IntegerField(blank=True, null=True)),
                ('packet_status', models.CharField(max_length=1)),
                ('ventor_id', models.CharField(blank=True, max_length=6, null=True)),
                ('imei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.devicetable')),
            ],
            options={
                'db_table': 'device_data_database',
            },
        ),
        migrations.CreateModel(
            name='commands_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=1)),
                ('imei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.devicetable')),
            ],
            options={
                'db_table': 'commands_table',
            },
        ),
    ]
