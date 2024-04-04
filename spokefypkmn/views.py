from django.shortcuts import render, redirect, get_object_or_404
from .operations import Pkmn, adicionar_pkmn_na_equipe
from spokefyapp.operations import get_playlist_tracks, get_playlist
from .forms import *
from django.http import HttpResponse
from .models import Equipe_Pkmn
from spokefyapp.models import Usuario_Spotify

# Os views aqui que estão presentes gerenciam como a comunicação do usuario com o server será realizada.
# Cada View interaje com o server e manda parametros para gerenciar a pagina HTML.
# Também são responsaveis em direicionar para qual URL o usuario estará.

# Views inicial para escolha dos pokemons para adicionar a equipe.
def home_page(request, user=None):
    form_equipe = EquipePkmnForm()
    equipes = Equipe_Pkmn.objects.filter(usuario=user)
    context= {
         'form' : form_equipe, 
         'pk' : False, 
         'user': user,
         'equipes': equipes
    }

    return render(request, 'spokefypkmn/profile.html', context)

# Views utilizado para mostrar ao usuario a playlist que foi gerada, juntamente a equipe.
def display_playlist(request, user, nome_equipe, playlist_id):
    equipe_atual=get_object_or_404(Equipe_Pkmn, usuario=user,nome_equipe=nome_equipe)
    playlist = get_playlist_tracks(user=equipe_atual.usuario,playlistId=equipe_atual.playlist)
    playlist_link = get_playlist(user=equipe_atual.usuario,playlistId=equipe_atual.playlist)
    context= {
         'equipe_atual': equipe_atual,
         'user': user,
         'playlist': playlist,
         'playlist_link': playlist_link['external_urls']['spotify']
    }
    print(playlist_link['external_urls']['spotify'])
    return render(request, 'spokefypkmn/playlist.html', context)

# Views que corresponde a escolha e adição do pokemon a equipe.
def criar_pkmn(request, nome_equipe=None, user=None,**kwargs):
    equipe_atual=get_object_or_404(Equipe_Pkmn, usuario=user,nome_equipe=nome_equipe)
    form_pkmn = PkmnForm()

    if request.method =='POST':
        # Utiliza o pokemon escolhido pelo usuario para ser criado chamando o PokeAPI. Caso dê erro, ele exclui a classe. Caso não, adiciona o pokemon a equipe.
        novo_pkmn = Pkmn(request.POST['pkmn'])
        if novo_pkmn.err:
            del novo_pkmn
        else:
            equipe_atual = adicionar_pkmn_na_equipe(equipe_atual=equipe_atual,
                                            pkmn=novo_pkmn)
    
    context = {'form' : form_pkmn, 
                 'equipe_atual' : equipe_atual      
            }
    return render(request, 'spokefypkmn/profile.html',context=context)

# Views utilizado para escolha do nome da equipe e a criação da equipe pokemon nova para o usuario.
def criar_equipe_pkmn(request,user=None):
        if request.method == "POST":
            userspotify = get_object_or_404(Usuario_Spotify, usuario=user)
            form_equipe = EquipePkmnForm()
            nova_equipe = form_equipe.save(commit=False)
            nova_equipe.nome_equipe = request.POST['nome_equipe']
            nova_equipe.usuario = userspotify
            nova_equipe.save()

            return redirect(nova_equipe,{
                'pk' : True,
                'equipe_atual': nova_equipe,
                })
        else:
            return redirect("pokemon-page", user)

# Views que permite a edição de uma equipe que ja existe e que não foi gerada sua playlist ainda.
def editar_equipe_pkmn(request, user, nome_equipe):
     if request.method == "GET":
        equipe_atual=get_object_or_404(Equipe_Pkmn, usuario=user,nome_equipe=nome_equipe)
        form_pkmn = PkmnForm()
        context = {
            'form' : form_pkmn, 
                'equipe_atual' : equipe_atual      
            }
        return render(request, 'spokefypkmn/profile.html',context=context)

# Views para excluir a equipe pokemon.
def excluir_equipe_pkmn(request, nome_equipe, user):
     equipe_atual=get_object_or_404(Equipe_Pkmn, usuario=user,nome_equipe=nome_equipe)
     equipe_atual.delete()

     return redirect("pokemon-page", user)

# Views para excluir um pokemon que está na equipe, mas só caso a playlist ainda não tenha sido gerada.
def excluir_pkmn(request, user, nome_equipe, nome_pkmn):
     equipe_atual=get_object_or_404(Equipe_Pkmn, usuario=user,nome_equipe=nome_equipe)
     equipe_atual.del_pkmn(nome_pkmn)

     return redirect(equipe_atual)