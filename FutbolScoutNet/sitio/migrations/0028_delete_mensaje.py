# Generated by Django 4.2.4 on 2023-10-14 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0027_remove_post_comentarios_alter_comment_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mensaje',
        ),
    ]
