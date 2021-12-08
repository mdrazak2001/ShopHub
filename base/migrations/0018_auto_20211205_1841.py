# Generated by Django 3.2.8 on 2021-12-05 13:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_product_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_id',
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, unique=True),
        ),
    ]
