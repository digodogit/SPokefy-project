from django import forms

class poke (object):
   def __init__(self):
       self.list = []

class PostForm(forms.Form):
    pkmn = forms.CharField()
    grind = poke()