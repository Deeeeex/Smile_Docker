from django.urls import path

from . import views

urlpatterns = [
    path("list_services/", views.list_services),
    path("create_service/", views.create_service),
    path("delete_service/", views.delete_service),
    path("update_service/", views.update_service),

]
