# Generated by Django 4.2.4 on 2023-09-01 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0013_post_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='multimedia',
            field=models.ImageField(blank=True, null=True, upload_to='UsersMultimedia'),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]
