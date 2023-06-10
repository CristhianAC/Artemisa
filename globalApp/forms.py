from django import forms

class ButtonSelector(forms.Form):
    choices = (
        ("0", "Dataset 1"),
        ("1", "Dataset 2"),
        ("2", "Dataset 3"),
        ("3", "Dataset 4"),
        ("4", "Dataset 5"),
        ("5", "Dataset 6"),
        ("6", "Dataset 7"),
        ("7", "Dataset 8"),
        ("8", "Dataset 9"),
        ("9", "Dataset 10"),
        ("10", "Dataset 11"),
        ("11", "Dataset 12")
    )
    dataset = forms.ChoiceField(choices= choices, label="Elige el dataset deseado")
class Searching(forms.Form):
    texto = forms.CharField(label="Nombre de especie")