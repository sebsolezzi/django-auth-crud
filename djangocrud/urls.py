"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('singup/',views.sing_up, name='singup'),
    path('tasks/',views.tasks, name='tasks'),
    path('tasks_complete/',views.tasks_complete, name='taskscomplete'),
    path('tasks/create',views.create_task, name='cratetask'),
    path('tasks/<int:task_id>',views.task_detail, name='taskdetail'),
    path('tasks/<int:task_id>/complete',views.task_complete, name='taskcomplete'),
    path('tasks/<int:task_id>/delete',views.task_delete, name='taskdelete'),
    path('logout/',views.log_out, name='logout'),
    path('login/',views.log_in, name='login'),
]
