from django.urls import path
from globalApp import views
urlpatterns = [
    path('', views.index),
    path('ArtemisaProyect', views.proyect),
]