# Generated by Django 4.2.4 on 2023-09-01 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0014_alter_post_multimedia_alter_post_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='user.png', upload_to='UsersMultimedia/profile_image'),
        ),
    ]