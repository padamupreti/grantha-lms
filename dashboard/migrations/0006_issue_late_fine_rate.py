# Generated by Django 4.2.2 on 2023-08-12 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_publisher_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='late_fine_rate',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
            preserve_default=False,
        ),
    ]