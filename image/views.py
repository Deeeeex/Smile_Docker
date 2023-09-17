from django.shortcuts import render

# Create your views here.
# image/views.py

from django.http import HttpResponse, JsonResponse
from docker import APIClient

# client = APIClient()
import docker

from image.utils import convert_bytes_to_human_readable

client = docker.from_env()


def list_images(request):
    user_id = request.POST.get('user_id')
    keyword = request.POST.get('keyword')
    images = client.images.list()
    # print(images)
    arr = []
    for image in images:
        name, version = image.tags[0].rsplit(':', 1)
        dic = {"id": image.short_id,
               "size": convert_bytes_to_human_readable(image.attrs['Size']),
               "create_time": image.attrs['Created'].split('T')[0],
               "names": name,
               "tag": version}
        # 需要添加按用户id筛选
        arr.append(dic)
    return JsonResponse(arr, safe=False)


def remove_image(request):
    image_id = request.POST.get('image_id')
    client.images.remove(image_id)
    return JsonResponse('remove success', safe=False)


def pull_image(request):
    client.images.pull(repository=request.form['repository'])
    return JsonResponse('pull success', safe=False)


def build_image(request):
    client.images.build(fileobj=request.files.get('dockerfile'), tag=request.form['tag'])
    return JsonResponse('build success', safe=False)
