import datetime
import math

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def administra_proyectos(self):
        return len(Proyecto.obtener_proyectos_por_administrador(self))

    @classmethod
    def crear_colaborador(cls, data):
        u = User.objects.create_user(username=data['username'], password=data['password'])
        u.save()
        return u.colaborador


def obtener_proyecto(id_proyecto):
    return Proyecto.objects.all().filter(id=id_proyecto).first()


class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=255)
    descripcion_proyecto = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    administrador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='proyecto_admin')
    colaboradores = models.ManyToManyField('Colaborador', null=True, blank=True, related_name='proyecto_colab')

    def __str__(self):
        return self.nombre_proyecto

    def obtener_administrador(self):
        return self.administrador

    def tiene_tareas(self):
        return len(self.obtener_tareas_de_proyecto()) > 0

    def obtener_tareas_de_proyecto(self):
        return Tarea.objects.filter(proyecto_id_id=self.id)

    def obtener_tareas_en_progreso(self):
        return [tarea for tarea in self.obtener_tareas_de_proyecto() if tarea.estado_tarea=='en progreso']

    @classmethod
    def obtener_proyectos_por_administrador(cls, user):
        return Proyecto.objects.all().filter(administrador_id=user.id)

    @classmethod
    def obtener_proyecto_por_id(cls, id):
        return Proyecto.objects.all().filter(id=id).first()

    def todas_las_tareas_finalizadas(self):
        return all(tarea.esta_finalizada() for tarea in self.obtener_tareas_de_proyecto())

    def obtener_tareas_atrasadas(self):
        tareas_atrasadas = [tarea for tarea in self.obtener_tareas_de_proyecto()
                            if tarea.esta_atrasada()]
        return tareas_atrasadas

    def todas_tareas_completadas(self):
        tareas_completadas = [tarea.esta_finalizada() for tarea
                              in self.obtener_tareas_de_proyecto()]
        return all(tareas_completadas)

    def obtener_tareas_por_retrasarse(self):
        return [tarea for tarea in self.obtener_tareas_de_proyecto() if tarea.va_a_retrasarse()]

    def obtener_tareas_por_finalizar(self):
        return [tarea for tarea in self.obtener_tareas_de_proyecto() if tarea.va_a_finalizar()]

    @classmethod
    def crear_proyecto(cls, datos):
        proyecto = Proyecto(
            nombre_proyecto=datos['nombre_proyecto'],
            descripcion_proyecto=datos['descripcion_proyecto'],
            fecha_inicio=datos['fecha_inicio'],
            fecha_fin=datos['fecha_fin'],
            administrador=datos['administrador']
        )
        proyecto.save()
        return proyecto


class Tarea(models.Model):
    nombre_tarea = models.CharField(max_length=50)
    codigo_tarea = models.CharField(max_length=30, unique=True)
    descripcion_tarea = models.TextField()
    prioridad_tarea = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    progreso = models.IntegerField(null=True)
    estado_tarea = models.CharField(max_length=30)
    proyecto_id = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    usuarios_asignados = models.ManyToManyField('Colaborador', null=True, blank=True)

    @classmethod
    def crear_tarea(cls, datos):
        tarea = Tarea(
            nombre_tarea=datos['nombre_tarea'],
            codigo_tarea=datos['codigo_tarea'],
            descripcion_tarea=datos['descripcion_tarea'],
            prioridad_tarea=datos['prioridad_tarea'],
            fecha_inicio=datos['fecha_inicio'],
            fecha_fin=datos['fecha_fin'],
            progreso=datos['progreso'],
            estado_tarea=datos['estado_tarea'],
            proyecto_id=datos['proyecto_id']
        )
        tarea.save()
        return tarea

    def iniciar(self):
        if self.puede_iniciarse():
            self.estado_tarea = 'en progreso'
            self.save()

    def __str__(self):
        return self.nombre_tarea

    def va_a_retrasarse(self):
        fecha_fin = datetime.date(self.fecha_fin.year, self.fecha_fin.month, self.fecha_fin.day)
        fecha_inicio = datetime.date(self.fecha_inicio.year, self.fecha_inicio.month, self.fecha_inicio.day)
        fecha_hoy = datetime.date.today()
        delta_inicio_fin = fecha_fin - fecha_inicio
        delta_inicio_hoy = fecha_hoy - fecha_inicio
        delta_hoy_fin = fecha_fin - fecha_hoy

        progreso_esperado = math.floor((delta_inicio_hoy.days * 100) / delta_inicio_fin.days)
        progreso_real = self.progreso
        return progreso_real < progreso_esperado and (delta_hoy_fin.days <= 1)

    def va_a_finalizar(self):
        fecha_fin = datetime.date(self.fecha_fin.year, self.fecha_fin.month, self.fecha_fin.day)
        fecha_hoy = datetime.date.today()
        delta_hoy_fin = fecha_fin - fecha_hoy
        return (delta_hoy_fin.days <= 1) and (not self.va_a_retrasarse())

    def tiene_colaboradores(self):
        return len(self.usuarios_asignados.all()) > 0

    def puede_iniciarse(self):
        return self.tiene_colaboradores()

    def tiene_muchos_colaboradores(self,colaboradores):
        return len(colaboradores)>3

    def asignar_colaboradores(self, colaboradores):
        if not self.tiene_muchos_colaboradores(colaboradores):
            self.usuarios_asignados.set(colaboradores)
            self.save()

    @classmethod
    def obtener_tarea_por_id(cls, selected):
        return Tarea.objects.all().filter(id=selected).first()



@receiver(post_save, sender=User)
def create_user_colaborador(sender, instance, created, **kwargs):
    if created:
        return Colaborador.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.colaborador.save()
