# Created by bryan at 11/1/2022
# language: es
# Enlace a la historia de usuario: https://gitlab.com/andrespalma02/proyectovv/-/issues/2
# -- FILE: features/environment.py

Característica: Visualización de tareas en un diagrama de Gantt
  Como administrador de un proyecto deseo visualizar, por medio de un diagrama de Gantt,
  el progreso de las tareas que se desarrollan en un proyecto,
  para tener un mayor control y facilidad al momento de tomar decisiones con respecto al proyecto.


  Esquema del escenario: No hay tareas
    Dado que he iniciado sesión como con las credenciales <username> y <contrasenia>
    Y soy administrador del proyecto con id <id_proyecto>
      | id_proyecto | nombre_proyecto | descripcion_proyecto | fecha_inicio | fecha_fin  |
      | 1           | Proyecto 1      | Proyecto 1           | 2022-02-10   | 2022-11-11 |
    Cuando no existen tareas para mostrar para el proyecto con id <id_proyecto>
    Entonces se mostrará la pantalla <pantalla>
    Ejemplos: Información del administrador
      | username | contrasenia | id_proyecto | pantalla         |
      | andres   | andres      | 1           | gantt_sin_tareas |


  Esquema del escenario: Una tarea está a punto de retrasarse
    Dado que he iniciado sesión como con las credenciales <username> y <contrasenia>
    Y soy administrador del proyecto con id <id_proyecto>
      | id_proyecto | nombre_proyecto | descripcion_proyecto | fecha_inicio | fecha_fin  |
      | 2           | Proyecto 1      | Proyecto 1           | 2022-10-10   | 2022-11-11 |
    Cuando existen tareas para mostrar para el proyecto
      | nombre_tarea | codigo_tarea | descripcion_tarea | prioridad_tarea | progreso | fecha_inicio | fecha_fin  | estado_tarea |
      | Tarea 1      | Ta-2-1       | Tarea 1           | 1               | 79       | 2022-02-20   | 2022-02-25 | en progreso  |
      | Tarea 2      | Ta-2-2       | Tarea 2           | 2               | 44       | 2022-02-20   | 2022-03-01 | en progreso  |
    Y existe al menos una tarea en el proyecto a punto de retrasarse
    Entonces estas tareas con estado <estado_tarea> se mostrarán en la pantalla <pantalla>
    Ejemplos: Información del administrador
      | username | contrasenia | id_proyecto | pantalla | estado_tarea          |
      | steven   | steven123   | 2           | gantt    | tareas_por_retrasarse |

  Esquema del escenario: Una tarea está a punto de finalizar
    Dado que he iniciado sesión como con las credenciales <username> y <contrasenia>
    Y soy administrador del proyecto con id <id_proyecto>
      | id_proyecto | nombre_proyecto | descripcion_proyecto | fecha_inicio | fecha_fin  |
      | 3           | Proyecto 2      | Proyecto 2           | 2022-10-10   | 2022-11-11 |
    Cuando existen tareas para mostrar para el proyecto
      | nombre_tarea | codigo_tarea | descripcion_tarea | prioridad_tarea | progreso | fecha_inicio | fecha_fin  | estado_tarea |
      | Tarea 1      | Ta-3-1       | Tarea 1           | 1               | 99       | 2022-02-28   | 2022-03-03 | en progreso  |
      | Tarea 2      | Ta-3-2       | Tarea 2           | 2               | 90       | 2022-10-18   | 2022-11-22 | en progreso  |
    Y una tareas del proyecto esté a punto de finalizar
    Entonces estas tareas con estado <estado_tarea> se mostrarán en la pantalla <pantalla>
    Ejemplos: Información del administrador
      | username | contrasenia | id_proyecto | pantalla | estado_tarea         |
      | andres   | andres      | 3           | gantt    | tareas_por_finalizar |

  Esquema del escenario: Mostrar tareas en progreso
    Dado que he iniciado sesión como con las credenciales <username> y <contrasenia>
    Y soy administrador del proyecto con id <id_proyecto>
      | id_proyecto | nombre_proyecto | descripcion_proyecto | fecha_inicio | fecha_fin  |
      | 4           | Proyecto 4      | Proyecto 4           | 2022-10-10   | 2022-11-11 |
    Cuando existen tareas para mostrar para el proyecto
      | nombre_tarea | codigo_tarea | descripcion_tarea | prioridad_tarea | progreso | fecha_inicio | fecha_fin  | estado_tarea |
      | Tarea 1      | Ta-3-1       | Tarea 1           | 1               | 90       | 2022-02-20   | 2022-02-26 | en progreso  |
      | Tarea 2      | Ta-3-2       | Tarea 2           | 2               | 90       | 2022-10-18   | 2022-11-22 | por iniciar  |
    Entonces solo se mostrarán las tareas con estado <estado_tarea> en la pantalla <pantalla>
    Ejemplos: Información del administrador
      | username | contrasenia | id_proyecto | pantalla | estado_tarea |
      | andres   | andres      | 3           | gantt    | en progreso  |

