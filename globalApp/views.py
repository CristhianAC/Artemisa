from django.shortcuts import render
from django.http import HttpResponse
from BackEnd.Procesos import Procesos
from .forms import ButtonSelector
procesos = Procesos()

# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    context = procesos.context
    context["formDs"] = ButtonSelector
    return render(request, "proyect.html", context)