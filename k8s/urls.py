from django.urls import path

from . import views

urlpatterns = [
    path("list_nodes/", views.list_nodes),
    path("list_pods/", views.list_pods),
    path("run_pods/", views.run_pod),
]
