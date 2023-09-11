from django.urls import path

from . import views

urlpatterns = [
    path("list_deployments/", views.list_deployments),
    path("delete_deployment/", views.delete_deployment),
    path("create_deployment/", views.create_deployment),
    path("update_deployment/", views.update_deployment),
]
