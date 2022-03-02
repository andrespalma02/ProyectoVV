from behave import step
from django.contrib.auth import authenticate

from planner.views import *


@step("que he iniciado sesión como con las credenciales {username} y {contrasenia}")
def step_impl(context, username, contrasenia):
    global colaborador
    Colaborador.crear_colaborador({'username': username, 'password': contrasenia})
    user=authenticate(username=username, password=contrasenia)
    colaborador = user.colaborador
    assert user.is_authenticated


@step("soy administrador del proyecto con id {id_proyecto}")
def step_impl(context, id_proyecto):
    global project
    project=Proyecto.obtener_proyecto_por_id(id_proyecto)
    for row in context.table:
        datos = {
            'nombre_proyecto': row['nombre_proyecto'],
            'descripcion_proyecto': row['descripcion_proyecto'],
            'fecha_inicio': row['fecha_inicio'],
            'fecha_fin': row['fecha_fin'],
            'administrador': colaborador
        }
    project = Proyecto.crear_proyecto(datos)
    assert project.obtener_administrador() == colaborador


"""
Pasos para la historia 2-hu08
"""


@step("no existen tareas para mostrar para el proyecto con id {proyecto_id}")
def step_impl(context, proyecto_id):
    project = Proyecto.obtener_proyecto_por_id(proyecto_id)
    assert project.tiene_tareas() is False


@step("se mostrará la pantalla {pantalla}")
def step_impl(context, pantalla):
    template = loader.get_template('vista_proyecto/' + pantalla + '.html')
    return template == obtener_template_project(project.id)


@step("existen tareas para mostrar para el proyecto")
def step_impl(context):
    global tareas
    for row in context.table:
        datos = {
            'nombre_tarea': row['nombre_tarea'],
            'codigo_tarea': row['codigo_tarea'],
            'descripcion_tarea': row['descripcion_tarea'],
            'prioridad_tarea': row['prioridad_tarea'],
            'fecha_inicio': row['fecha_inicio'],
            'fecha_fin': row['fecha_fin'],
            'progreso': row['progreso'],
            'estado_tarea': row['estado_tarea'],
            'proyecto_id': project
        }
        tareas = Tarea.crear_tarea(datos)
    assert project.tiene_tareas() is True


@step("existe al menos una tarea en el proyecto a punto de retrasarse")
def step_impl(context):
    assert len(project.obtener_tareas_por_retrasarse()) > 0


@step("una tareas del proyecto esté a punto de finalizar")
def step_impl(context):
    assert len(project.obtener_tareas_por_finalizar()) > 0


@step("estas tareas con estado {estado_tarea} se mostrarán en la pantalla {pantalla}")
def step_impl(context, estado_tarea, pantalla):
    contexto = generar_contexto_gantt(project.id)
    template = loader.get_template('vista_proyecto/gantt.html')
    return estado_tarea in contexto.keys() and template == obtener_template_project(project.id)


@step("solo se mostrarán las tareas con estado {estado_tarea} en la pantalla {pantalla}")
def step_impl(context, estado_tarea, pantalla):
    tareas = project.obtener_tareas_en_progreso()
    tareas_en_progreso = [tarea for tarea in tareas if tarea.estado_tarea == 'en progreso']
    assert tareas == tareas_en_progreso
"""
Pasos para la historia 7-hu06
"""





@step("creo una tarea en el proyecto")
def step_impl(context):
    for row in context.table:
        datos = {
            'nombre_tarea': row['nombre_tarea'],
            'codigo_tarea': row['codigo_tarea'],
            'descripcion_tarea': row['descripcion_tarea'],
            'prioridad_tarea': row['prioridad_tarea'],
            'fecha_inicio': row['fecha_inicio'],
            'fecha_fin': row['fecha_fin'],
            'progreso': row['progreso'],
            'estado_tarea': row['estado_tarea'],
            'proyecto_id': project.id
        }
        Tarea.crear_tarea(datos)
    assert project.tiene_colaboradores()


@step("existen colaboradores en el proyecto")
def step_impl(context):
    global colaboradores
    colaboradores = []
    for row in context.table:
        data = {
            'username': row['username'],
            'password': row['password']
        }
        colaboradores.append(Colaborador.crear_colaborador(data))
    assert len(colaboradores) > 0




@step("se ha creado una tarea en el proyecto sin asignar colaboradores")
def step_impl(context):
    global tarea
    for row in context.table:
        datos = {
            'nombre_tarea': row['nombre_tarea'],
            'codigo_tarea': row['codigo_tarea'],
            'descripcion_tarea': row['descripcion_tarea'],
            'prioridad_tarea': row['prioridad_tarea'],
            'fecha_inicio': row['fecha_inicio'],
            'fecha_fin': row['fecha_fin'],
            'progreso': row['progreso'],
            'estado_tarea': row['estado_tarea'],
            'proyecto_id': project
        }
        tarea = Tarea.crear_tarea(datos)
    assert tarea.tiene_colaboradores() is False

@step("asigno un colaborador")
def step_impl(context):
    tarea.asignar_colaboradores(colaboradores)
    assert tarea.tiene_colaboradores()


@step("se intente iniciar la tarea")
def step_impl(context):
    tarea.iniciar()
    return tarea


@step("se intente asignar {numero} colaboradores")
def step_impl(context, numero):
    tarea.asignar_colaboradores(colaboradores)


@step("el estado de la tarea permanecerá igual")
def step_impl(context):
    assert tarea.estado_tarea=='por iniciar'


@step("no se permitirá asignar dicho numero de colaboradores")
def step_impl(context):
    assert tarea.tiene_muchos_colaboradores(colaboradores)