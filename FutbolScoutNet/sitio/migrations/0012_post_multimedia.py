# Generated by Django 4.2.4 on 2023-08-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0011_profile_edad'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='multimedia',
            field=models.ImageField(null=True, upload_to='UsersMultimedia'),
        ),
    ]
