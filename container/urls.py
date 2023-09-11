from django.urls import path

from . import views

urlpatterns = [
    path("list_containers/", views.list_containers),
    path("run_container/", views.run_container),
    path("rename_container/", views.rename_container),
    path("restart_container/", views.restart_container),
    path("start_container/", views.start_container),
    path("stop_container/", views.stop_container),
    path("remove_container/", views.remove_container),
]
