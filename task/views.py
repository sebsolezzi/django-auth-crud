#get_object_or_404 usamos para buscar un elento si no lo encuentra regresa un 404
from django.shortcuts import render,redirect, get_object_or_404
#importar HttpResponse para poder enviar respuestas http
from django.http import HttpResponse
#importar UserCreationForm para poder crear un formulario directamente  y AuthenticationForm para logear
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
#importar User para usar el modelo de usuario para guardar en la base de datos
from django.contrib.auth.models import User
#Importar login para crear una cookie de login
from django.contrib.auth import login,logout, authenticate
#login_required  para proteger rutas q se necesita estar logueado
from django.contrib.auth.decorators import login_required 
#importamos IntegrityError para informar error de que ese usuario ya existe
from django.db import IntegrityError
from django.utils import timezone
#Importamos nuestro propio formulario creado
from .forms import TaskForm
#Importamos el modelo de las tareas para poder obtenerlas y mostrarlas a la pagina
from .models import Task

# Create your views here.
def home(request):
    return render(request,'home.html')

def sing_up(request):
    #render el primer parametro que requiere es el request y segundo la pagina web q debe estar en templates
    #pasamos un diccionario con parametros en este caso pasamos el UserCreationForm
    if request.method == 'GET':
        return render(request,'singup.html',{'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #si las contrseñas coinciden creamos un objeto usuario
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                  return render(request,'singup.html',{
                      'form':UserCreationForm,
                      'error':"Usuario ya existe"
                      })            
        return render(request,'singup.html',{
                      'form':UserCreationForm,
                      'error':"Las contraseñas no coinciden"
                      })

@login_required
def tasks(request):
    #Buscamos q solo nos regrese las tareas del usuario q está logeado
    tasks = Task.objects.filter(user=request.user,datecompleated__isnull=True)
    return render(request,'tasks.html',{'tasks':tasks})

@login_required
def tasks_complete(request):
    #Buscamos q solo nos regrese las tareas del usuario q está logeado
    tasks = Task.objects.filter(user=request.user,datecompleated__isnull=False).order_by('-datecompleated')
    return render(request,'tasks.html',{'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html',{'form':TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user #usuario q esta logeado hay q agregarlo a la tabla
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html',{'form':TaskForm,'error':'Complete con datos validos'})

@login_required
def task_detail(request,task_id):
    #Buscamos en la base de datos el task q corresponde a ese id de tarea y tambien sea del user q esta conenctado y luego se lo pasamos al formulario
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id,user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{'form':form,'task':task})
    else:
        try:
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html',{'form':form,'task':task,'error':"Erro al actulizar"})

@login_required
def task_complete(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleated = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def log_in(request):
    if request.method == 'GET':
        return render(request,'login.html',{'form':AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request,username= request.POST['username'], password=request.POST['password'])
        #La funcion authenticate regresa un usuario si no lo encuentra regresa None
        if user is None:
            return render(request,'login.html',{'form':AuthenticationForm,'error':"Usuario o contraseña incorrectos"})
        else:
            #si conincide usuario y contraseña lo logueamos y lo redireccionamos a los tasks
            login(request,user)
            return redirect('tasks')

@login_required    
def log_out(request):
    logout(request)
    return redirect('home')