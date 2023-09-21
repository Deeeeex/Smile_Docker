import json
import random
import string

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
import yaml

config.load_kube_config()


def list_deployments(request):
    label_selector = "user=1"
    keyword = request.POST.get('search')
    ret = client.AppsV1Api().list_namespaced_deployment('default',
                                                        label_selector=label_selector)
    arr = []
    for i in ret.items:
        if keyword != "":
            if keyword not in i.metadata.name:
                continue
        service_name = i.metadata.name.replace("deployment", "service")
        pod_name = i.metadata.name[len("deployment-"):]
        label_selector_pod = "user=" + pod_name
        service_list = client.CoreV1Api(). \
            list_namespaced_service('default',
                                    field_selector=f"metadata.name={service_name}")
        service = service_list.items[0]
        ret = client.CoreV1Api().list_pod_for_all_namespaces(watch=False,
                                                             label_selector=label_selector_pod)

        try:
            pod = ret.items[0]
            containerId = pod.status.container_statuses[0].container_id[len("docker://"):len("docker://") + 12],
            image = pod.spec.containers[0].image
        except Exception as e:
            containerId = "null"
            image = "null"

        dic = {'name': i.metadata.name,
               'creation_timestamp': i.metadata.creation_timestamp,
               'namespace': i.metadata.namespace,
               'available_replicas': i.status.available_replicas,
               'replicas': i.status.replicas,
               'nodePort': service.spec.ports[0].node_port,
               'containerPort': service.spec.ports[0].port,
               'containerId': containerId,
               'image': image}
        arr.append(dic)

    return JsonResponse(arr, safe=False)


def delete_deployment(request):
    name = request.POST.get('name')
    namespace = 'default'
    client.AppsV1Api().delete_namespaced_deployment(name="deployment-" + name, namespace=namespace)
    client.CoreV1Api().delete_namespaced_service(name="service-" + name, namespace=namespace)
    return JsonResponse('delete success', safe=False)


def create_deployment(request):
    container_port = request.POST.get('container_port')
    node_port = random.randint(30000, 32767)
    environment = json.loads(request.POST.get('environment'))
    deployment_manifest = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': "deployment-" + request.POST.get('name'),
            'labels': {
                'user': '1',
                'deployment': "deployment-" + request.POST.get('name')
            }
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'user': request.POST.get('name')
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'user': request.POST.get('name')
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
                'user': request.POST.get('name')
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


def stop_deployment(request):
    deployment_name = request.POST.get('name')
    scale_body = {"spec": {"replicas": 0}}
    client.AppsV1Api().patch_namespaced_deployment_scale(name=deployment_name,
                                                         namespace="default",
                                                         body=scale_body)

    return JsonResponse('stop success', safe=False)


def run_deployment(request):
    deployment_name = request.POST.get('name')
    scale_body = {"spec": {"replicas": 1}}
    client.AppsV1Api().patch_namespaced_deployment_scale(name=deployment_name,
                                                         namespace="default",
                                                         body=scale_body)
    return JsonResponse('restart success', safe=False)
