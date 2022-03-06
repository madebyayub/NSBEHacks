from django.urls import path, include
from main.views import index, problem

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('problem/<str:id>/', problem, name='problem'),
]
