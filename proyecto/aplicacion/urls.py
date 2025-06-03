from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

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

    path("estudiantes/",  views.EstudianteList.as_view() , name="estudiantes"),
    path("estudianteCreate/",  views.EstudianteCreate.as_view() , name="estudianteCreate"),
    path("estudianteUpdate/<int:pk>/",  views.EstudianteUpdate.as_view() , name="estudianteUpdate"),
    path("estudianteDelete/<int:pk>/",  views.EstudianteDelete.as_view() , name="estudianteDelete"),

    path('registro/', views.register, name="registro"),
    path('login/', views.loginRequest, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.editarPerfil, name='perfil'),
    path('agregar_avatar/', views.agregarAvatar, name="agregar_avatar"),
]
