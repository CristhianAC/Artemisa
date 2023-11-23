from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import modelEjecute



# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    
    if request.method == 'POST':
        form = modelEjecute(request.POST)
        if form.is_valid():
            pass
        return HttpResponseRedirect('/ArtemisaProyect')
    else:
        form = modelEjecute()
    context = {'form': form}
    return render(request, "proyect.html", context)