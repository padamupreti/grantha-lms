# Generated by Django 4.2.2 on 2023-07-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_issue_request_alter_issue_returned_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='is_fulfilled',
            field=models.BooleanField(default=False),
        ),
    ]
