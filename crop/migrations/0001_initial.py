# Generated by Django 5.1.7 on 2025-03-23 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CropListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(max_length=100)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(choices=[('kg', 'Kilograms'), ('quintal', 'Quintal'), ('ton', 'Ton')], max_length=10)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
