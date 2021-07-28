# Generated by Django 3.2.4 on 2021-07-24 12:10

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_live_location_table_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicledetails',
            name='vehicle_no',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name='user_vehicle_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renewal_of_data', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('renewal_of_insurance', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('renewal_of_fitness', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('renewal_of_pollution', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('renewal_of_tax', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('driver_mobile', models.CharField(help_text='Phone number without Country Code', max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('vehicle_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.vehicledetails', to_field='vehicle_no')),
            ],
            options={
                'db_table': 'user_vehicle_services',
            },
        ),
    ]