from django.urls import path

from . import views

urlpatterns = [
    path("list_applications/", views.list_applications),
    path("create_application/", views.create_application),
    path("delete_application/", views.delete_application),
]
