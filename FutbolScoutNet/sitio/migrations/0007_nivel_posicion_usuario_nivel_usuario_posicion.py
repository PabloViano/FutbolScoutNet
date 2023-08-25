# Generated by Django 4.2.4 on 2023-08-25 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0006_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.IntegerField(choices=[(1, 'Amateur'), (2, 'Semiprofesional'), (3, 'Profesional')])),
            ],
        ),
        migrations.CreateModel(
            name='Posicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion', models.IntegerField(choices=[(1, 'Arquero'), (2, 'Defensa'), (3, 'Mediocampista'), (4, 'Delantero')])),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='nivel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sitio.nivel'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='posicion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sitio.posicion'),
        ),
    ]