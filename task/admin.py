from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created" ,)
# Register your models here. Registramos nuestro modelo de tareas para que se vea en la pagina Admin
admin.site.register(Task,TaskAdmin)