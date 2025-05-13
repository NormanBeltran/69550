from django.shortcuts import render
from django.http import HttpResponse

from .models import Curso
import datetime, random 

# Create your views here.
def saludo(request):
    saludar = "Bienvenidos al curso de Python / Django"
    return HttpResponse(saludar)

def bienvenida(request):
    hoy = datetime.datetime.now()
    saludo = f"""
    <html>
    <h1>Bienvenidos al curso de Python / Django</h1>
    <h2>Hoy es {hoy}</h2>
    <h3>Gracias por visitarnos</h3>
    </html>
    """
    return HttpResponse(saludo) 

def bienvenido(request, nombre, apellido):
    hoy = datetime.datetime.now()
    saludo = f"""
    <html>
    <h1>Bienvenido {nombre} {apellido} al curso de Python / Django</h1>
    <h2>Hoy es {hoy}</h2>
    <h3>Gracias por visitarnos</h3>
    </html>
    """
    return HttpResponse(saludo) 

def bienvenido_tpl(request):
    hoy = datetime.datetime.now()
    contexto = {"fecha": hoy, "nombre": "Juan", "apellido": "Perez"}
    return render(request, "aplicacion/bienvenido.html", contexto )

def nuevo_curso(request):
    comision = random.randint(10000, 99999)
    nombre = random.choices(["Python", "Java", "C#", "JavaScript", "PHP", "Cobol", "Pascal"], k=1)[0]
    curso = Curso(nombre=nombre, comision=comision)
    curso.save()    
    return render(request, "aplicacion/nuevo_curso.html", {"curso": nombre, "comision": comision})   