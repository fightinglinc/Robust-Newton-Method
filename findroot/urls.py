from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.find_root, name='find_root')
]
