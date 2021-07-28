# Generated by Django 3.2.4 on 2021-07-26 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210724_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='commands_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=1)),
                ('imei', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.devicetable')),
            ],
            options={
                'db_table': 'commands_table',
            },
        ),
    ]
