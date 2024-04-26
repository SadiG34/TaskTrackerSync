import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfweb.settings')
django.setup()

from django.db import IntegrityError
from TaskAppWeb.models import *

import http.client
import json
conn = http.client.HTTPSConnection("ru.yougile.com")

headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer ******" #токен yougile для получения задач
    }

conn.request("GET", "/api-v2/tasks", headers=headers)

res = conn.getresponse()
data = res.read()
data = data.decode("utf-8") #расшифровал из байтов в строку
result = json.loads(data) #из строки в dict. здесь хранятся задачи из yougile


yougile_tasks = result['content']


import requests

url = 'https://testcompany1.planfix.ru/rest/task/list'
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer ********',#ввести pf токен чтобы получить задачи
    'Content-Type': 'application/json'
}
data = {
  "offset": 0,
  "pageSize": 100,
  "filters": [
    {
      "type": 51,
      "operator": "equal",
      "value": [
        1,
        2
      ]
    }
  ],
  "fields": "id,name,description"
}

response = requests.post(url, headers=headers, json=data)

planfix_tasks = response.json()['tasks']
def save_yougile_tasks():
    encoded_json = json.dumps(yougile_tasks) # в json
    decoded_json = encoded_json.encode().decode('unicode-escape') # более читаемый вид
    credit = TaskYougile.objects.create(dict_info=decoded_json) #сохранил в бд



# for task in TaskYougile.objects.all():
#     print(task.dict_info)
#
# for task in TaskPlanfix.objects.all():
#     print(task.dict_info)



def save_planfix_tasks():
    encoded_json = json.dumps(planfix_tasks) # в json
    decoded_json = encoded_json.encode().decode('unicode-escape') # более читаемый вид
    credit = TaskPlanfix.objects.create(dict_info=decoded_json) #сохранил в бд


def create_task_in_planfix(yougile_task, planfix_tasks):
    if yougile_task["title"] not in [task["name"] for task in planfix_tasks]:
        new_task = {"name": yougile_task["title"], "description": yougile_task.get("description", "")}
        planfix_tasks.append(new_task)
        url = 'https://testcompany1.planfix.ru/rest/task/'
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ***************', #тут pf токен нужно ввести
            'Content-Type': 'application/json'
        }
        data = {
            "name": new_task['name'],
            "description": new_task['description']
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            return "Task created successfully in Planfix"
        else:
            return f"Failed to create task in Planfix. Status code: {response.status_code}, Response: {response.text}"


def create_task_in_yougile(planfix_task, yougile_tasks, token):
    if planfix_task["name"] not in [task["title"] for task in yougile_tasks]:
        new_task = {"title": planfix_task["name"], "description": planfix_task.get("description", "")}
        yougile_tasks.append(new_task)

        import http.client
        import json

        conn = http.client.HTTPSConnection("ru.yougile.com")

        payload = {
            "title": planfix_task['name'],
            "columnId": "******", #колонка где будут сохраняться задачи
            "description": planfix_task.get('description', ''),
            "archived": False,
            "completed": False,
            "deadline": {"deadline": 1653029146646, "startDate": 1653028146646, "withTime": True},
            "checklists": [
                {"title": "list 1", "items": [{"title": "option 1", "isCompleted": False},
                                              {"title": "option 2", "isCompleted": False}]
                }
            ]
        }

        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }

        conn.request("POST", "/api-v2/tasks", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

token = '********' # my yougile token
token2 = '********' #my pf token
def sync_tasks(yougile_tasks, planfix_tasks):
    dict_yougile = {task["title"]: task for task in yougile_tasks}
    dict_planfix = {task["name"]: task for task in planfix_tasks}

    for title, task in dict_yougile.items():
        create_task_in_planfix(task, planfix_tasks)

    for name, task in dict_planfix.items():
        create_task_in_yougile(task, yougile_tasks, token)


