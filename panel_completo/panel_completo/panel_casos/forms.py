from django import forms
from .models import Agente, Casuistica

class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['nombre']

class CasuisticaForm(forms.ModelForm):
    class Meta:
        model = Casuistica
        fields = ['nombre', 'peso']

class AgenteCasuisticaForm(forms.Form): #nuevo formulario
    agente_form = forms.ModelChoiceField(queryset=Agente.objects.all(), widget=forms.Select, empty_label="Selecciona un Agente")
    nombre_casuistica = forms.CharField(max_length=200)
    peso_casuistica = forms.IntegerField()