from django.shortcuts import render

# Create your views here.
# image/views.py

from django.http import HttpResponse, JsonResponse
from docker import APIClient

# client = APIClient()
import docker

client = docker.from_env()


def list_images(request):
    images = client.images.list()
    print(images)
    arr = []
    for image in images:
        dic = {"attrs": image.attrs, "id": image.id, "labels": image.labels, "short_id": image.short_id,
               "tags": image.tags}
        arr.append(dic)
    return JsonResponse(arr)


def remove_image(request):
    image_id = request.POST['image_id']
    client.images.remove(image_id)
    return JsonResponse('remove success', safe=False)


def pull_image(request):
    client.images.pull(repository=request.form['repository'])
    return JsonResponse('pull success', safe=False)


def build_image(request):
    client.images.build(fileobj=request.files.get('dockerfile'), tag=request.form['tag'])
    return JsonResponse('build success', safe=False)
