from django.shortcuts import render
from django.http import HttpResponse
from BackEnd.Procesos import Procesos
from .forms import ButtonSelector, Searching
procesos = Procesos()

# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    if request.method == "GET":
        context = procesos.obternerHTML()
        context["formDs"] = ButtonSelector
        context["search"] = Searching
        return render(request, "proyect.html", context)
    else:
        
        context = procesos.obternerHTML(request.POST['dataset'])
        context["formDs"] = ButtonSelector
        context["search"] = Searching
        return render(request, "proyect.html", context)