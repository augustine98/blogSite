# Generated by Django 3.1.2 on 2021-05-18 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0013_auto_20210518_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='upvotes',
            field=models.ManyToManyField(blank=True, default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), related_name='post_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
