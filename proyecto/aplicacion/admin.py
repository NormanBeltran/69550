from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Curso)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Entregable)