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
        if request.POST['dataset'] is not None:
            context = procesos.obternerHTML(int(request.POST['dataset']))
        if request.POSTes['texto'] is not None:
            context = procesos.solicitarInfoEspecie(request.POSTes['texto'])
        context["formDs"] = ButtonSelector
        context["search"] = Searching
        return render(request, "proyect.html", context)