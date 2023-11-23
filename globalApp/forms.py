from django import forms

class modelEjecute(forms.Form):
    name = forms.CharField(label='Digita el nombre de una especie', max_length=100)