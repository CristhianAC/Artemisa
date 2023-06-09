from django.shortcuts import render
from django.http import HttpResponse
from BackEnd.Procesos import Procesos

procesos = Procesos()

# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    context = procesos.context
    
    return render(request, "proyect.html", context)