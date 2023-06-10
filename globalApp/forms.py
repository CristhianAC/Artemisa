from django import forms

class ButtonSelector(forms.Form):
    choices = (
        ("1", "Dataset 1"),
        ("2", "Dataset 2"),
        ("3", "Dataset 3"),
        ("4", "Dataset 4"),
        ("5", "Dataset 5"),
        ("6", "Dataset 6"),
        ("7", "Dataset 7"),
        ("8", "Dataset 8"),
        ("9", "Dataset 9"),
        ("10", "Dataset 10"),
        ("11", "Dataset 11"),
        ("12", "Dataset 12")
    )
    Dataset = forms.ChoiceField(choices= choices, label="Elige el dataset deseado")