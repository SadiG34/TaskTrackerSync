from rest_framework import generics
from django.shortcuts import render
from .models import *
from .serializer import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import save_yougile_tasks, save_planfix_tasks, sync_tasks, planfix_tasks, yougile_tasks
from django.http import JsonResponse
import json


class TaskAPIView(APIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        return TaskYougile.objects.all()

    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def save_tasks_for_yougile(request):
    if request.method == 'POST':
        save_yougile_tasks()
        return HttpResponse('Yougile задачи сохранены успешно')
    else:
        return render(request, 'TaskAppWeb/save_tasks_for_yougile.html', {})


def save_tasks_for_planfix(request):
    if request.method == 'POST':
        save_planfix_tasks()
        return HttpResponse('Planfix задачи сохранены успешно')
    else:
        return render(request, 'TaskAppWeb/save_tasks_for_planfix.html', {})


def home(request):
    if request.method == 'POST':
        sync = False #возможно здесь ошибка

        if 'sync_planfix' in request.POST:
            for task_pf in planfix_tasks:
                if task_pf["name"] not in [task["title"] for task in yougile_tasks]:
                    sync = True
                    break
        elif 'sync_yougile' in request.POST:
            for task_yg in yougile_tasks:
                if task_yg["title"] not in [task["name"] for task in planfix_tasks]:
                    sync = True
                    break

        if sync:
            sync_tasks(yougile_tasks, planfix_tasks)
            response_data = {'status': 'Синхронизация завершена'}
            return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
        else:
            response_data = {'status': 'Нет несоответствий для синхронизации'}
            return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

    elif request.method == 'GET':
        return render(request, 'TaskAppWeb/home.html')

    else:
        response_data = {'status': 'Метод не разрешен'}
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json", status=405)
