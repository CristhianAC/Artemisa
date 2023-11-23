from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import modelEjecute
from Modelo.Modelo import generarModelo as Modelo
import os 

# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    showimage = False
    if request.method == 'POST':
        form = modelEjecute(request.POST)
        if form.is_valid():
            modelo = Modelo(form.cleaned_data['name'])
            showimage = True
        return HttpResponseRedirect('/ArtemisaProyect')
    else:
        form = modelEjecute()
        showimage = False
    context = {'form': form, 'showimage': showimage}
    return render(request, "proyect.html", context)