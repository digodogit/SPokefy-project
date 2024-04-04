from django.shortcuts import render, redirect, get_object_or_404,reverse
from .operations import *
from django.http import HttpResponse
from .forms import *
from requests import Request


# Os views aqui que estão presentes gerenciam como a comunicação do usuario com o server será realizada.
# Cada View interaje com o server e manda parametros para gerenciar a pagina HTML.
# Também são responsaveis em direicionar para qual URL o usuario estará.


# Pagina inicial do site.
def home_page(request):
    return render(request, 'spokefyapp/index.html')

# View responsavel por direcionar o usuario para a pagian de autenticação do Spotify.
def spotify_log(request, format=None):
        credentials = open_json()
        
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': credentials["scopes"],
            'response_type': 'code',
            'redirect_uri': credentials["redirect_uri"],
            'client_id': credentials["client_id"]
        }).prepare().url

        return redirect(url)

# View responsavel por utilizar os dados recebidos após a autorização de login do spotify.   
def spotify_callback(request, format=None):
    if not request.session.exists(request.session.session_key):
        request.session.create()
        request.session["usuario_id"]=None

    if request.session["usuario_id"]:
        usuario_info = check_token(session=request.session)
    else:
        code = request.GET.get('code')
        usuario_info = gerar_token(code=code, session=request.session)
    
    return redirect(usuario_info.get_absolute_url(), permanent=True) 
    
# View responsavel pelo gerenciamento da criação da playlist após a criação da equipe e a adição dos pokemons.
def criar_playlist(request, nome_equipe=None, user=None, **kwargs):
    if request.method =="POST":
        usuariospotify= get_object_or_404(Usuario_Spotify, usuario=user)
        equipe_atual =  usuariospotify.equipe_pkmn_set.get(nome_equipe=nome_equipe)
        tracks_vetor = []
        equipe_atual.playlist = create_playlist(user=user, nomePlaylist=equipe_atual.nome_equipe)
        equipe_atual.save(update_fields=['playlist'])
        for genero in equipe_atual.get_genero():
            tracks = get_recommendations(user=equipe_atual.usuario, 
                                                limit=3,
                                                genres=genero["genero"])
            for track_uri in tracks["tracks"]:
                tracks_vetor.append(track_uri["uri"])

        add_tracks_playlist(user=equipe_atual.usuario,
                            playlist_id=equipe_atual.playlist, tracks=tracks_vetor)
        
        return redirect(reverse("display-playlist",kwargs={'nome_equipe': equipe_atual.nome_equipe,
                                                   'user': user,
                                                   'playlist_id':equipe_atual.playlist}))
    else:
         return render(request,'spokefypkmn/profile.html')
   



