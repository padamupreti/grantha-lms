# Generated by Django 4.2.2 on 2023-06-26 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='returned_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
