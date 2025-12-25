from django.urls import path
from .views import enter_chat

urlpatterns = [
    path("enter/", enter_chat),
]
