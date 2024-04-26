import http.client
import json
conn = http.client.HTTPSConnection("ru.yougile.com")

headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer THjge2L5O6M5Klop-din+SNirVjm2xwOpbKF6WKDM+tGEWe-EwcD3ijyP5zPEwL7"
    }

conn.request("GET", "/api-v2/tasks", headers=headers)

res = conn.getresponse()
data = res.read()
data = data.decode("utf-8") #расшифровал из байтов в строку
result = json.loads(data) #из строки в dict. здесь хранятся задачи из yougile

for i in result['content']:
    print(i['title'])