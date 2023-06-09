from django.shortcuts import render
from django.http import HttpResponse
from BackEnd.Procesos import Procesos

procesos = Procesos()

# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    db = procesos.datasets[2]
    fig = procesos.graficos.variacionConteoEspeciesEndemicas(db)
    fig = procesos.graficos.temporalBiodiversidadAlpha(db)
    fig = procesos.graficos.temporalBiodiversidadBeta(db)
    fig = procesos.graficos.variacionEspeciesEndemicas(db)
    fig = procesos.graficos.variacionConteoEspeciesEndemicas(db)
    fig = procesos.graficos.proporcionEspeciesEndemicas(db)
    fig = procesos.cartoficos.generarMapaDistribucionEndemicas(db)
    procesos.cartoficos.generarMapaLocalizacionMuestras(db, 'Arremon schlegeli')
    context = {'chart': fig.to_html()}
    return render(request, "proyect.html", context)