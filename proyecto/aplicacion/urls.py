from django.urls import path
from . import views

urlpatterns = [
    path("saludo/",  views.saludo, name="saludo"),
    path("bienvenida/",  views.bienvenida, name="bienvenida"),
    path("bienvenido/<nombre>/<apellido>/",  views.bienvenido, name="bienvenido"),
    path("bienvenido_tpl/",  views.bienvenido_tpl, name="bienvenido_tpl"),
    path("nuevo_curso/",  views.nuevo_curso, name="nuevo_curso"),
]
