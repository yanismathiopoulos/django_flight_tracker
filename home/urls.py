from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('result/', views.calculator_output, name='calculator_out'),
]
