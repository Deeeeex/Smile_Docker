from django.shortcuts import render

# Create your views here.
# image/views.py

from django.http import HttpResponse, JsonResponse
from docker import APIClient

# client = APIClient()
import docker

from image.utils import *

client = docker.from_env()


def list_images(request):
    user_id = request.POST.get('user_id')
    keyword = request.POST.get('keyword')
    images = client.images.list()
    # print(images)
    arr = []
    for image in images:
        print(image.tags)
        name, version, tags = get_image_info(image)
        # 暂停用户隔离改为True
        flag = True
        for tag in tags:
            if tag == user_id:
                flag = True
        dic = {"id": image.short_id,
               "size": convert_bytes_to_human_readable(image.attrs['Size']),
               "create_time": image.attrs['Created'],
               "names": name,
               "version": tags}
        # 需要添加按用户id筛选
        if flag is True:
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
