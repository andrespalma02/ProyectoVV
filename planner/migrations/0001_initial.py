# Generated by Django 4.0 on 2021-12-30 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=255)),
                ('descripcion_proyecto', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tarea', models.CharField(max_length=50)),
                ('codigo_tarea', models.CharField(max_length=30, unique=True)),
                ('descripcion_tarea', models.TextField()),
                ('prioridad_tarea', models.CharField(max_length=30)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado_tarea', models.CharField(max_length=30)),
                ('proyecto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('nombre_usuario', models.CharField(max_length=30)),
                ('correo', models.CharField(max_length=30)),
                ('contrasenia', models.CharField(max_length=30)),
                ('rol', models.CharField(max_length=30)),
                ('tarea', models.ManyToManyField(to='planner.Tarea')),
            ],
        ),
    ]
