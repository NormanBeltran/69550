from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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

@login_required
def nuevo_curso(request):
    comision = random.randint(10000, 99999)
    nombre = random.choices(["Python", "Java", "C#", "JavaScript", "PHP", "Cobol", "Pascal"], k=1)[0]
    curso = Curso(nombre=nombre, comision=comision)
    curso.save()    
    return render(request, "aplicacion/nuevo_curso.html", {"curso": nombre, "comision": comision})   

@login_required
def cursos(request):
    cursos = Curso.objects.all()
    return render(request, "aplicacion/cursos.html", {"cursos": cursos})

@login_required
def profesores(request):
    profesores = Profesor.objects.all()
    return render(request, "aplicacion/profesores.html", {"profesores": profesores})

@login_required
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

@login_required
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

class EstudianteList(LoginRequiredMixin, ListView):
    model = Estudiante

class EstudianteCreate(LoginRequiredMixin, CreateView):
    model = Estudiante
    fields = ["nombre", "apellido", "email"]    
    success_url = reverse_lazy("estudiantes")

class EstudianteUpdate(LoginRequiredMixin, UpdateView):
    model = Estudiante
    fields = ["nombre", "apellido", "email"]
    success_url = reverse_lazy("estudiantes")

class EstudianteDelete(LoginRequiredMixin, DeleteView):
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
            #_______ Buscar Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            #______________________________________________________________            
            return render(request, "aplicacion/index.html")
        else:
            return redirect(reverse_lazy('login'))
    else:
        miForm = AuthenticationForm()

    return render(request, "aplicacion/login.html", {"form": miForm})

# ___________  edit Perfil de usuario ______________
"""
@login_required # con este decorador exigimos que el usuario esté logueado para utilizar esta view
def editarPerfil(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'aplicacion/editarPerfil.html', {'form': form})
"""

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy("bienvenido_tpl"))
    else:
        miForm = UserEditForm(instance=usuario)
    return render(request, "aplicacion/editarPerfil.html", {"form": miForm})

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)
        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            imagen = miForm.cleaned_data["imagen"]
            #_________ Borrar avatares viejos
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #__________________________________________
            avatar = Avatar(user=usuario, imagen=imagen)
            avatar.save()

            #_________ Enviar la imagen al home
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            #____________________________________________________
            return redirect(reverse_lazy("bienvenido_tpl"))
    else:
        miForm = AvatarForm()
    return render(request, "aplicacion/agregarAvatar.html", {"form": miForm})    
