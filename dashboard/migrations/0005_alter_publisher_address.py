# Generated by Django 4.2.2 on 2023-07-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_request_is_fulfilled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='address',
            field=models.CharField(default='Kathmandu, Nepal', max_length=50),
            preserve_default=False,
        ),
    ]
