#Para crear nuestros formularios personalizados basados en nuestros modelos
from django.forms import ModelForm
from .models import Task


class TaskForm(ModelForm):
     class Meta:
         model = Task
         fields = ['title','description','important']