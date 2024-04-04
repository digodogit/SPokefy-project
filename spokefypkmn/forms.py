from django import forms
from .models import Equipe_Pkmn
from django.forms.widgets import TextInput

#Forms baseado no models Equipe_Pkmn. Onde é escolhido o nome da equipe. 
class EquipePkmnForm(forms.ModelForm):
    
    class Meta:
        model = Equipe_Pkmn
        fields = ["nome_equipe"]
        labels = {"nome_equipe": "Nome da Equipe", }
        widgets = {"nome_equipe":TextInput(attrs={"class":"form-control"})} 
        localized_fields = ['usuario']
        
#Forms para escolher o pokemons que irá ser adicionado a equipe.
class PkmnForm(forms.Form):
    pkmn = forms.CharField(label="Nome do Pokemon", max_length=25,
                           widget=TextInput(attrs={"class":"form-control"}))