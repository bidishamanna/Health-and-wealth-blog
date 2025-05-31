from django.urls import path
from subscriber import views

urlpatterns = [
    path("post_subscriber/", views.post_subscriber, name='post_subscriber'),
    path("get_subscriber/", views.get_subscriber, name='get_subscriber'),
    path("delete_subscriber", views.delete_subscriber, name='delete_subscriber'),
]

