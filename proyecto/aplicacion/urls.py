from django.urls import path
from . import views

urlpatterns = [
    path("saludo/",  views.saludo, name="saludo"),
    path("bienvenida/",  views.bienvenida, name="bienvenida"),
    path("bienvenido/<nombre>/<apellido>/",  views.bienvenido, name="bienvenido"),
    path("bienvenido_tpl/",  views.bienvenido_tpl, name="bienvenido_tpl"),

    path("cursos/",  views.cursos, name="cursos"),
    path("curso_form/",  views.cursoForm, name="curso_form"),

    path("profesores/",  views.profesores, name="profesores"),
    path("profesor_form/",  views.profesorForm, name="profesor_form"),

    path("nuevo_curso/",  views.nuevo_curso, name="nuevo_curso"),
]
