from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import *
from .forms import *
import datetime, random 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

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

def cursos(request):
    cursos = Curso.objects.all()
    return render(request, "aplicacion/cursos.html", {"cursos": cursos})

def profesores(request):
    profesores = Profesor.objects.all()
    return render(request, "aplicacion/profesores.html", {"profesores": profesores})

def profesorForm(request):
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            email = form.cleaned_data["email"]
            profesion = form.cleaned_data["profesion"]
            profesor = Profesor(nombre=nombre, apellido=apellido, email=email, profesion=profesion)
            profesor.save()
            profesores = Profesor.objects.all()
            return render(request, "aplicacion/profesores.html", {"profesores": profesores})
    else:
        form = ProfesorForm()
    return render(request, "aplicacion/profesor_form.html", {"form": form})


def cursoForm(request):
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            comision = form.cleaned_data["comision"]
            curso = Curso(nombre=nombre, comision=comision)
            curso.save()
            cursos = Curso.objects.all()
            return render(request, "aplicacion/cursos.html", {"cursos": cursos})
    else:
        form = CursoForm()
    return render(request, "aplicacion/curso_form.html", {"form": form})

# _________________ CBV CRUD __________________

class EstudianteList(ListView):
    model = Estudiante

class EstudianteCreate(CreateView):
    model = Estudiante
    fields = ["nombre", "apellido", "email"]    
    success_url = reverse_lazy("estudiantes")

class EstudianteUpdate(UpdateView):
    model = Estudiante
    fields = ["nombre", "apellido", "email"]
    success_url = reverse_lazy("estudiantes")

class EstudianteDelete(DeleteView):
    model = Estudiante
    success_url = reverse_lazy("estudiantes")        

# _______________ Registracion / Login / Logout __________________

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        if miForm.is_valid():
            miForm.save()
            return redirect(reverse_lazy('bienvenido_tpl'))
    else:
        miForm = RegistroForm()

    return render(request, "aplicacion/registro.html", {"form": miForm})   

def loginRequest(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        clave = request.POST["password"]
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return render(request, "aplicacion/index.html")
        else:
            return redirect(reverse_lazy('login'))
    else:
        miForm = AuthenticationForm()

    return render(request, "aplicacion/login.html", {"form": miForm})