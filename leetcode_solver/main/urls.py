from django.urls import path, include
from main.views import index, problem

urlpatterns = [
    path('', index),
    path('<int:id>/', problem)
]