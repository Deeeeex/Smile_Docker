from django.shortcuts import render

# Create your views here.
# k8s/views.py

from kubernetes import client, config
from django.http import HttpResponse, JsonResponse

config.load_kube_config()


def list_nodes(request):
    ret = client.CoreV1Api().list_node()
    arr = []
    for i in ret.items:
        dic = {'kind': i.kind,
               'name': i.metadata.name,
               'namespace': i.metadata.namespace,
               'creation_timestamp': i.metadata.creation_timestamp,
               'allocatable': i.status.allocatable,
               'phase': i.status.phase,
               }
        print(i.status.capacity)
        arr.append(dic)

    return JsonResponse(arr, safe=False)


def list_pods(request):
    ret = client.CoreV1Api().list_pod_for_all_namespaces(watch=False)
    arr = []
    for i in ret.items:
        dic = {'namespace': i.metadata.namespace, 'name': i.metadata.name,
               'creation_timestamp': i.metadata.creation_timestamp, 'pod_ip': i.status.pod_ip}
        container_statuses = []
        for status in i.status.container_statuses:
            s = {'name': status.name, 'container_id': status.container_id, 'image_id': status.image_id,
                 'image': status.image, 'ready': status.ready}
            container_statuses.append(s)
        dic['container_statuses'] = container_statuses
        dic['node_name'] = i.spec.node_name
        arr.append(dic)

    # 处理pods,转成dict
    return JsonResponse(arr, safe=False)



