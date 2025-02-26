# Generated by Django 5.1 on 2024-08-24 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mi_app', '0009_remove_comentario_clase_remove_perfil_clases_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=20)),
                ('Apellido', models.CharField(max_length=20)),
                ('Usuario', models.CharField(max_length=25, unique=True)),
                ('Correo', models.CharField(max_length=50, unique=True)),
                ('Contraseña', models.CharField(max_length=20)),
                ('Ncuenta', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clases', models.ManyToManyField(related_name='perfiles', to='mi_app.clase')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to='mi_app.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='mi_app.clase')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='mi_app.usuario')),
            ],
        ),
    ]
