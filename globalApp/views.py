from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import modelEjecute
from Modelo import Modelo


# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    modelo = Modelo()
    if request.method == 'POST':
        form = modelEjecute(request.POST)
        if form.is_valid():
            pass
        return HttpResponseRedirect('/ArtemisaProyect')
    else:
        form = modelEjecute()
    context = {'form': form}
    return render(request, "proyect.html", context)