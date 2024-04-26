"""
URL configuration for drfweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from TaskAppWeb.views import TaskAPIView, save_tasks_for_yougile, save_tasks_for_planfix, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('api/v1/tasklist', TaskAPIView.as_view()),
    path('save-tasks/', save_tasks_for_yougile, name='save_tasks_for_yougile'),
    path('save-tasks2/', save_tasks_for_planfix, name='save_tasks_for_planfix'),
]
