# Generated by Django 5.2 on 2025-06-16 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_gazebomodel_alter_gazeboserviceoption_gazebo_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Installation Type Name')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='installation_type_images/', verbose_name='Installation Type Photo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Installation Type Description')),
            ],
            options={
                'verbose_name': 'Installation Type',
                'verbose_name_plural': 'Installation Types',
            },
        ),
        migrations.AlterField(
            model_name='installationserviceoption',
            name='location',
            field=models.CharField(choices=[('INDOOR', 'Indoor'), ('OUTDOOR', 'Outdoor'), ('BOTH', 'Both')], max_length=20, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='installationserviceoption',
            name='installation_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_options', to='services.installationtype', verbose_name='Installation Type'),
        ),
    ]
