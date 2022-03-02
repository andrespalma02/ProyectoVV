import django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.middleware.csrf import rotate_token

from planner.models import Proyecto, Tarea, Colaborador


def obtener_template_project(selected):
    proyecto = Proyecto.obtener_proyecto_por_id(selected)
    if proyecto.tiene_tareas():
        return loader.get_template('vista_proyecto/gantt.html')
    else:
        return loader.get_template('vista_proyecto/gantt_sin_tareas.html')


def generar_contexto_gantt(project_id):
    context = {}
    project = Proyecto.obtener_proyecto_por_id(project_id)
    if project is not None:
        context['proyecto'] = project

    lista_tareas = project.obtener_tareas_en_progreso()
    if lista_tareas is not None:
        context['lista_tareas'] = lista_tareas

    lista_proyectos = Proyecto.objects.all()
    if lista_proyectos:
        context['lista_proyectos'] = lista_proyectos

    tareas_por_retrasarse = project.obtener_tareas_por_retrasarse()
    if tareas_por_retrasarse:
        context['tareas_por_retrasarse'] = tareas_por_retrasarse

    tareas_por_finalizar = project.obtener_tareas_por_finalizar()
    if tareas_por_finalizar:
        context['tareas_por_finalizar'] = tareas_por_finalizar

    return context


@login_required
def obtener_vista_principal(request):
    projects = Proyecto.objects.all()
    if request.method == 'POST':
        selected = int(request.POST.get('proyecto'))
    else:
        selected = projects[0].id
    template = obtener_template_project(selected)
    context = generar_contexto_gantt(selected)
    return HttpResponse(template.render(context, request))


@login_required
def obtener_vista_anadir_colaborador(request, tarea_id=None):
    selected = int(tarea_id)
    tarea = Tarea.obtener_tarea_por_id(selected)
    if request.POST.get('colaboradores'):
        tarea = Tarea.obtener_tarea_por_id(int(request.POST.get('tarea')))
        tarea.asignar_colaboradores(request.POST.get('colaboradores'))
        return obtener_vista_iniciar_tarea(request, tarea.id)
    proyecto = Proyecto.obtener_proyecto_por_id(tarea.proyecto_id.id)
    template = loader.get_template('vista_tarea/anadir_colaborador.html')
    colaboradores = Colaborador.objects.all()
    context = {
        'proyecto': proyecto,
        'tarea': tarea,
        'colaboradores': colaboradores
    }
    return HttpResponse(template.render(context, request))


def obtener_vista_iniciar_tarea(request, id_tarea):
    tarea = Tarea.obtener_tarea_por_id(id_tarea)
    if tarea:
        tarea.iniciar()
        if tarea.estado_tarea == 'en progreso':
            django.middleware.csrf.get_token(request)
            request = HttpRequest()
            return obtener_vista_backlog(request)
        else:
            request.method = 'GET'
            return obtener_vista_anadir_colaborador(request, id_tarea)
    else:
        request.method = 'GET'
        return obtener_vista_backlog(request)


def obtener_vista_backlog(request):
    if request.method == 'POST':
        tarea_id = request.POST.get('tarea')
        return obtener_vista_iniciar_tarea(request, tarea_id)
    else:
        tareas = Tarea.objects.all()
        tareas_iniciadas = [tarea for tarea in tareas if tarea.estado_tarea == 'en progreso']
        tareas_por_iniciar = [tarea for tarea in tareas if tarea not in tareas_iniciadas]

        contexto = {
            'tareas_por_iniciar': tareas_por_iniciar,
            'tareas_iniciadas': tareas_iniciadas
        }
        template = loader.get_template('vista_tarea/backlog_tareas.html')
        return HttpResponse(template.render(contexto, request))
