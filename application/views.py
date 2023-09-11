from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
import yaml


# Create your views here.
def list_applications(request):
    ns_list = client.CoreV1Api().list_namespace()
    arr = []
    for ns_item in ns_list.items:
        ns = ns_item.metadata.name
        deployment_list = client.AppsV1Api().list_namespaced_deployment(ns)
        service_list = client.CoreV1Api().list_namespaced_service(ns)

        dic = {'namespace': ns}

        deployments = []
        for i in deployment_list.items:
            d = {'name': i.metadata.name, 'creation_timestamp': i.metadata.creation_timestamp,
                 'namespace': i.metadata.namespace, 'available_replicas': i.status.available_replicas,
                 'replicas': i.status.replicas}
            deployments.append(d)
        dic['deployments'] = deployments

        services = []
        for i in service_list.items:
            d = {'name': i.metadata.name, 'creation_timestamp': i.metadata.creation_timestamp,
                 'namespace': i.metadata.namespace, 'cluster_ip': i.spec.cluster_ip,
                 'external_i_ps': i.spec.external_i_ps, 'type': i.spec.type}
            ports = []
            for p in i.spec.ports:
                tem = {'node_port': p.node_port, 'port': p.port, 'protocol': p.protocol}
                ports.append(tem)
            d['ports'] = ports
            services.append(d)
        dic['services'] = services
        arr.append(dic)
    return JsonResponse(arr, safe=False)


def create_application(request):
    deployment_config = request.POST.get('deployment_config[]')
    service_config = request.POST.get('service_config[]')

    client.CoreV1Api().create_namespace(
        body=client.V1Namespace(metadata=client.V1ObjectMeta(name=request.form['namespace'])))

    for config in deployment_config:
        dep = yaml.safe_load(config)
        client.AppsV1Api().create_namespaced_deployment(body=dep, namespace=request.form['namespace'])

    for config in service_config:
        dep = yaml.safe_load(config)
        client.CoreV1Api().create_namespaced_service(body=dep, namespace=request.form['namespace'])

    return JsonResponse('create success', safe=False)


def delete_application(request):
    namespace = request.POST['namespace']
    client.CoreV1Api().delete_namespace(name=namespace)
    return JsonResponse('delete success', safe=False)
