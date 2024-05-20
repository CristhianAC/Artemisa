from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import modelEjecute

import os 

# Create your views here.
def index(request):
    return render(request,"index.html")
def proyect(request):
    showimage = True
    if request.method == 'POST':
        form = modelEjecute(request.POST)
        if form.is_valid():
            try:
                
                showimage = True
            except Exception as e:
                print(e)
                showimage = False
        return HttpResponseRedirect('/ArtemisaProyect')
    else:
        form = modelEjecute()
        
    
    context = {'form': form, 'showImage': showimage}
    print(context)
    return render(request, "proyect.html", context)