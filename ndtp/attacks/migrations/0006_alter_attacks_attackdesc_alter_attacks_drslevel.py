# Generated by Django 4.2 on 2023-04-17 12:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attacks', '0005_alter_attacks_attackdesc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attacks',
            name='attackDesc',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='attacks',
            name='drsLevel',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(0)]),
        ),
    ]
