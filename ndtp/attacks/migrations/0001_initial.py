# Generated by Django 4.2 on 2023-04-08 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttacksCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=50)),
                ('createDate', models.DateTimeField(verbose_name='date created')),
                ('categoryDesc', models.CharField(max_length=200)),
            ],
        ),
    ]
