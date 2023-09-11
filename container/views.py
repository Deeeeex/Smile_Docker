from django.shortcuts import render

# Create your views here.
# container/views.py

from django.http import HttpResponse, JsonResponse
from docker import APIClient
import docker

# client = APIClient()
client = docker.from_env()


def list_containers(request):
    containers = client.containers.list(all=True)
    arr = []
    for container in containers:
        dic = {"id": container.id, 'name': container.name,
               'image': {'id': container.image.id, 'tags': container.image.tags}, "labels": container.labels,
               "short_id": container.short_id, "status": container.status}
        arr.append(dic)
    # 处理containers,转成dict
    return JsonResponse(arr, safe=False)


def run_container(request):
    command = request.POST.get('command[]')
    environment = request.POST.get('environment[]')
    container_ports = request.POST.get('container_ports[]')
    host_posts = request.POST.get('host_posts[]')
    volumes = request.POST.get('volumes[]')
    ports = {}
    for cp, hp in zip(container_ports, host_posts):
        ports[cp] = hp

    client.containers.run(image=request.form['image'], name=request.form['name'], command=command,
                          environment=environment, ports=ports, volumes=volumes, detach=True)
    return JsonResponse({'status': 'success'})


def rename_container(request):
    container = client.containers.get(request.form['container_id'])
    container.rename(request.form['new_name'])
    return JsonResponse({'status': 'success'})


def restart_container(request):
    container = client.containers.get(request.form['container_id'])
    container.restart()
    return JsonResponse({'status': 'success'})


def start_container(request):
    container = client.containers.get(request.form['container_id'])
    container.start()
    return JsonResponse({'status': 'success'})


def stop_container(request):
    container = client.containers.get(request.form['container_id'])
    container.stop()
    return JsonResponse({'status': 'success'})


def remove_container(request):
    container = client.containers.get(request.form['container_id'])
    container.remove()
    return JsonResponse({'status': 'success'})
