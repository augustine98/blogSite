# Generated by Django 3.0.3 on 2020-10-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201028_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='score',
            field=models.IntegerField(default=-10),
        ),
    ]
