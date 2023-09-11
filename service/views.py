from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
import yaml


def list_services(request):
    ret = client.CoreV1Api().list_service_for_all_namespaces()
    arr = []
    for i in ret.items:
        dic = {}
        dic['name'] = i.metadata.name
        dic['creation_timestamp'] = i.metadata.creation_timestamp
        dic['namespace'] = i.metadata.namespace
        dic['cluster_ip'] = i.spec.cluster_ip
        dic['external_i_ps'] = i.spec.external_i_ps
        dic['type'] = i.spec.type
        ports = []
        for p in i.spec.ports:
            tem = {'node_port': p.node_port, 'port': p.port, 'protocol': p.protocol}
            ports.append(tem)
        dic['ports'] = ports
        arr.append(dic)
    return JsonResponse(arr, safe=False)


def create_service(request):
    service = yaml.safe_load(request.files.get('config'))
    client.CoreV1Api().create_namespaced_service(body=service, namespace=request.form['namespace'])
    return JsonResponse('create success', safe=False)


def delete_service(request):
    name = request.POST['name']
    namespace = request.POST['namespace']
    client.CoreV1Api().delete_namespaced_service(name=name, namespace=namespace)
    return JsonResponse('delete success', safe=False)


def update_service(request):
    service = yaml.safe_load(request.files.get('config'))
    client.CoreV1Api().replace_namespaced_service(body=service, name=request.form['name'],
                                                  namespace=request.form['namespace'])
    return JsonResponse('update success', safe=False)



