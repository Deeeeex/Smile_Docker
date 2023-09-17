import os
import shutil
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
    client.images.remove(image_id, force=True)
    return JsonResponse({
        "msg": "删除镜像成功"
    })


def pull_image(request):
    client.images.pull(request.POST.get('name'), tag=request.POST.get('tags'))
    return JsonResponse('拉取成功', safe=False)


def pull_image_repository(request):
    tag = request.POST.get('tags')
    print(tag)
    client.images.pull(request.POST.get('repository'), tag=tag)
    return JsonResponse('拉取成功', safe=False)


def build_image(request):
    dockerfile = request.FILES.get('dockerfile')
    tags = request.POST.get('tags')

    # 将 Dockerfile 保存到临时目录中
    temp_dir = tempfile.mkdtemp()
    dockerfile_path = os.path.join(temp_dir, 'Dockerfile')
    with open(dockerfile_path, 'wb') as file:
        for chunk in dockerfile.chunks():
            file.write(chunk)

    try:
        # 使用临时目录路径作为构建路径
        client.images.build(path=temp_dir, tag=tags)
        response = 'dockerfile构建成功'
    except Exception as e:
        response = f'构建镜像时出现错误: {str(e)}'

    # 删除临时目录及其内容
    shutil.rmtree(temp_dir)

    return JsonResponse(response, safe=False)
