# Generated by Django 4.2.4 on 2023-10-22 18:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0032_comment_estado_post_estado_profile_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='edad',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
