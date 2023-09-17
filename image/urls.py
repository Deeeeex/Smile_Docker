from django.urls import path

from . import views

urlpatterns = [
    path("list_images/", views.list_images),
    path("remove_image/", views.remove_image),
    path("pull_image/", views.pull_image),
    path("build_image/", views.build_image),
    path("pull_image_registry/", views.pull_image_registry),
]
