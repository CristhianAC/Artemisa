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
        context["conclusiones"] = procesos.ia.generarConclusion(procesos.dataset)
        context["formDs"] = ButtonSelector
        context["search"] = Searching
        return render(request, "proyect.html", context)
    else:
       
        try:
            if request.POST['dataset'] is not None:
                context = procesos.obternerHTML(int(request.POST.get('dataset',False)))
                context["conclusiones"] = procesos.ia.generarConclusion(procesos.dataset)
        except:
            print("No encontró seleccion de dataset") 
        try:
            if request.POST['texto'] is not None:
                try:
                    context = procesos.solicitarInfoEspecie(request.POST['texto'])
                except:
                    print("No se encontró la especie")
        except:
            print("No se encontró el texto")
        
        context["formDs"] = ButtonSelector
        context["search"] = Searching
        return render(request, "proyect.html", context)