# Generated by Django 4.2.4 on 2023-08-23 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0003_usuario_delete_perfil'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Publicacion',
            new_name='Post',
        ),
    ]
