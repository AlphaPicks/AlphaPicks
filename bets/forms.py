from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(max_length=100)
class Prediccion(forms.Form):
    prediccion = forms.DecimalField()   