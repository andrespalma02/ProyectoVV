# Created by bryan at 11/1/2022
# language: es
  #Link a la historia de usuario: https://gitlab.com/andrespalma02/proyectovv/-/issues/7
Característica: Asignación de colaboradores a una tarea

  Como administrador de proyecto deseo asignar uno o varios colaboradores de un proyecto a una misma tarea,
  para controlar el flujo de ejecución de dicha tarea.

  Esquema del escenario: Tarea iniciada sin colaboradores
    Dado que he iniciado sesión como con las credenciales <username> y <contrasenia>
    Y soy administrador del proyecto con id <id_proyecto>
      | id_proyecto | nombre_proyecto | descripcion_proyecto | fecha_inicio | fecha_fin  |
      | 1           | Proyecto 1      | Proyecto 1           | 2022-10-10   | 2022-11-11 |
    Y se ha creado una tarea en el proyecto sin asignar colaboradores
      | nombre_tarea | codigo_tarea | descripcion_tarea | prioridad_tarea | progreso | fecha_inicio | fecha_fin  | estado_tarea |
      | Tarea 1      | Ta-1-1       | Tarea 1           | 1               | 90       | 2022-10-10   | 2022-11-11 | por iniciar  |
    Cuando se intente iniciar la tarea
    Entonces el estado de la tarea permanecerá igual
    Ejemplos: Información del administrador
      | username | contrasenia | id_proyecto | pantalla
      | andres   | andres      | 1           | anadir_colaborador


  Esquema del escenario: Asignar más de 3 colaboradores
    Dado que he iniciado sesión como con las credenciales <username> y <contrasenia>
    Y soy administrador del proyecto con id <id_proyecto>
      | id_proyecto | nombre_proyecto | descripcion_proyecto | fecha_inicio | fecha_fin  |
      | 2           | Proyecto 2      | Proyecto 2           | 2022-10-10   | 2022-11-11 |
    Y se ha creado una tarea en el proyecto sin asignar colaboradores
      | nombre_tarea | codigo_tarea | descripcion_tarea | prioridad_tarea | progreso | fecha_inicio | fecha_fin  | estado_tarea |
      | Tarea 1      | Ta-2-1       | Tarea 1           | 1               | 90       | 2022-10-10   | 2022-11-11 | por iniciar    |
    Y existen colaboradores en el proyecto
      | username | password     |
      | steven   | zsfdfggh3456 |
      | andres2  | sf34fgtg45gy |
      | steven2  | zsfdfggh3456 |
      | andres3  | sf34fgtg45gy |
    Cuando se intente asignar <numero> colaboradores
    Entonces no se permitirá asignar dicho numero de colaboradores
    Ejemplos: Información del administrador
      | username | contrasenia | id_proyecto | numero |
      | andres   | andres      | 2           | 4      |









