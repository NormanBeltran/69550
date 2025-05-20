from  django import forms

class CursoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre del curso", required=True)
    comision = forms.IntegerField(required=True)

class ProfesorForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre del profesor", required=True)
    apellido = forms.CharField(max_length=50, label="Apellido del profesor", required=True)
    email = forms.EmailField(required=True)
    profesion = forms.CharField(max_length=50, label="Profesión", required=True)