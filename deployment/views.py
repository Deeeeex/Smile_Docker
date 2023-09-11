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
        dic = {}
        dic['name'] = i.metadata.name
        dic['creation_timestamp'] = i.metadata.creation_timestamp
        dic['namespace'] = i.metadata.namespace
        dic['available_replicas'] = i.status.available_replicas
        dic['replicas'] = i.status.replicas
        arr.append(dic)

    return JsonResponse(arr, safe=False)


def delete_deployment(request):
    name = request.POST['name']
    namespace = request.POST['namespace']
    client.AppsV1Api().delete_namespaced_deployment(name=name, namespace=namespace)
    return JsonResponse('delete success', safe=False)


def create_deployment(request):
    dep = yaml.safe_load(request.files.get('config'))
    client.AppsV1Api().create_namespaced_deployment(body=dep, namespace=request.form['namespace'])
    return JsonResponse('create success', safe=False)


def update_deployment(request):
    dep = yaml.safe_load(request.files.get('config'))
    client.AppsV1Api().replace_namespaced_deployment(body=dep, name=request.form['name'],
                                                     namespace=request.form['namespace'])
    return JsonResponse('update success', safe=False)


