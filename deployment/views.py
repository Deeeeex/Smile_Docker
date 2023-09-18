import json
import random

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
import yaml

config.load_kube_config()


def list_deployments(request):
    ret = client.AppsV1Api().list_deployment_for_all_namespaces()
    arr = []
    for i in ret.items:
        dic = {'name': i.metadata.name,
               'creation_timestamp': i.metadata.creation_timestamp,
               'namespace': i.metadata.namespace,
               'available_replicas': i.status.available_replicas,
               'replicas': i.status.replicas}
        arr.append(dic)

    return JsonResponse(arr, safe=False)


def delete_deployment(request):
    name = request.POST.get('name')
    namespace = request.POST.get('namespace')
    client.AppsV1Api().delete_namespaced_deployment(name="deployment-"+name, namespace=namespace)
    client.CoreV1Api().delete_namespaced_service(name="service-"+name, namespace=namespace)
    return JsonResponse('delete success', safe=False)


def create_deployment(request):
    container_port = request.POST.get('container_port')
    node_port = random.randint(30000, 32767)
    environment = json.loads(request.POST.get('environment'))
    deployment_manifest = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': "deployment-"+request.POST.get('name'),
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'user': 'a'
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'user': 'a'
                    }
                },
                'spec': {
                    'containers': [{
                        'name': request.POST.get('name'),
                        'image': request.POST.get('image'),
                        'ports': [{
                            'containerPort': int(container_port),
                        }],
                        'env': environment,
                        'imagePullPolicy': 'IfNotPresent'
                    }]
                }
            },
        }
    }

    service_manifest = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': "service-" + request.POST.get('name'),
            'labels': {
                'service': request.POST.get('name')
            }
        },
        'spec': {
            'type': 'NodePort',
            'ports': [{
                'port': int(container_port),
                'nodePort': node_port,
                'protocol': 'TCP',
                'name': 'anyway'
            }],
            'selector': {
                'user': '1'
            }
        }
    }

    try:
        client.AppsV1Api().create_namespaced_deployment(body=deployment_manifest, namespace="default")
        client.CoreV1Api().create_namespaced_service(body=service_manifest, namespace="default")
        response = '工作负载创建成功'
    except Exception as e:
        response = f'工作负载创建失败{str(e)}'
        print(e)
    return JsonResponse(response, safe=False)


def update_deployment(request):
    dep = yaml.safe_load(request.files.get('config'))
    client.AppsV1Api().replace_namespaced_deployment(body=dep, name=request.form['name'],
                                                     namespace=request.form['namespace'])
    return JsonResponse('update success', safe=False)


