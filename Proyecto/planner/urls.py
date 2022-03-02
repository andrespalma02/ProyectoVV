from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.obtener_vista_principal, name='index'),
	path('tareas',views.obtener_vista_backlog, name='backlogtareas'),
	path('tareas/anadir-colaborador',views.obtener_vista_anadir_colaborador, name='anadircolab')
]
urlpatterns += [
	path('accounts/', include('django.contrib.auth.urls')),
]
