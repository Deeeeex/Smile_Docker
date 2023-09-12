import json

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


def run_pod(request):
    core_v1_api = client.CoreV1Api()
    environment = json.loads(request.POST.get('environment[]'))
    container_ports = request.POST.get('container_ports[]')
    host_posts = request.POST.get('host_posts[]')
    # volumes = request.POST.get('volumes[]')

    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'pod',
            'labels': {
                'user': '1'
            }
        },
        'spec': {
            'containers': [{
                'name': request.POST.get('name'),
                'image': request.POST.get('image'),
                'ports': [{
                    'containerPort': int(container_ports),
                    'hostPort': int(host_posts)
                }],
                'env': environment
            }]
        }
    }
    ret = core_v1_api.create_namespaced_pod(body=pod_manifest, namespace='default')

    api_client = client.ApiClient()
    serialized_response = api_client.sanitize_for_serialization(ret)
    return JsonResponse({'status': 'success',
                         'ret': serialized_response})
