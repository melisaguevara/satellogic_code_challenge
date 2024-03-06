# Generated by Django 5.0.2 on 2024-03-05 20:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('resources', django.contrib.postgres.fields.ArrayField(
                    base_field=models.CharField(max_length=50), size=None)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(choices=[('IN_QUEUE', 'In Queue'), ('PROCESSING', 'Processing'), (
                    'PROCESSED', 'Processed')], default='IN_QUEUE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
