from django.db import models


# Create your models here.
class Proyecto(models.Model):
	nombre_proyecto = models.CharField(max_length=255)
	descripcion_proyecto = models.TextField()
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()


class Tarea(models.Model):
	nombre_tarea = models.CharField(max_length=50)
	codigo_tarea = models.CharField(max_length=30, unique=True)
	descripcion_tarea = models.TextField()
	prioridad_tarea = models.CharField(max_length=30)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()
	estado_tarea = models.CharField(max_length=30)
	proyecto_id = models.ForeignKey(Proyecto, on_delete=models.CASCADE)


