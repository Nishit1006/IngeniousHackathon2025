# Generated by Django 5.1.7 on 2025-03-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_application', '0006_add_created_at_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 