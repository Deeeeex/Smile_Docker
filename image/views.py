import os
import tempfile

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
        dic = {"id": image.short_id.split(":")[1],
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
    return JsonResponse({
        "msg": "删除镜像成功"
    })


def pull_image(request):
    client.images.pull(request.POST.get('name'), tag=request.POST.get('tags'))
    return JsonResponse('拉取成功', safe=False)


def pull_image_repository(request):
    client.images.pull(tag=request.POST.get('tags'),
                       repository=request.POST.get('repository'))
    return JsonResponse('拉取成功', safe=False)


def build_image(request):
    dockerfile = request.FILES.get('dockerfile')
    tags = request.POST.get('tags')

    # 将文件对象保存到临时文件中
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in dockerfile.chunks():
            temp_file.write(chunk)

    try:
        # 使用临时文件路径来构建镜像
        client.images.build(path=temp_file.name, tag=tags)
        response = 'dockerfile构建成功'
    except Exception as e:
        response = f'构建镜像时出现错误: {str(e)}'

    # 删除临时文件
    os.remove(temp_file.name)

    return JsonResponse(response, safe=False)
