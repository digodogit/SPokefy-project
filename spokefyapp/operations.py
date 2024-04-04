from .models import Usuario_Spotify
from django.utils import timezone
from datetime import timedelta
import base64
import requests
import json


# Operations são funções e classes usados para auxiliar o que está sendo usado no Views.
# É uma forma de deixar mais limpo o código para melhor gerenciamento e entendimento do que está sendo feito.

# Abrir arquivo json.
def open_json():
        with open('data.json', 'r') as file:
            return json.load(file)

# Função responsavel por pedir para o SpotifyAPI um novo token de autenticação para o usuario.
def gerar_token(code, session):
    url='https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code
    }
    response = requests_call(method="POST", url=url, params=token_data)

    session["token_acesso"] = response['access_token']
    session["token_novo"] = response['refresh_token']
    session["expires_in"] = response['expires_in']
    session["usuario_id"] = pegar_user(session["token_acesso"])

    return adicionar_token(session=session)

# Função que checa se o usuario que está querendo acessar já está cadastrado e precisa renovar seu token ou é um usuario novo.
def check_token(session):
    usuario_info =  Usuario_Spotify.objects.pegar_usuario(user=session["usuario_id"])
    if usuario_info.expires_in <=timezone.now():
        return refresh_token(session)
    else: 
       
        return usuario_info 

# Função para renovar o token de acesso do usuario.
def refresh_token(session):
    url='https://accounts.spotify.com/api/token'
    print(session)
    
    token_data = {
            'grant_type':'refresh_token',
            'refresh_token': session["token_novo"]
        }
    response = requests_call(method="POST", url=url, params=token_data)

    session["expires_in"] = response['expires_in']
    session["token_acesso"] = response['access_token']

    return adicionar_token(session=session)

# Adiciona o token de acesso novo ao usuario. Caso ele não exista, o usuario é criado pelo model Usuario_Spotify e adicionado ao banco de dados.
def adicionar_token(session):
    usuario_info =  Usuario_Spotify.objects.pegar_usuario(user=session["usuario_id"])
    expires_in = timezone.now() + timedelta(seconds=session["expires_in"])

    if usuario_info:
        usuario_info.token_acesso= session["token_acesso"]  
        usuario_info.token_novo = session["token_novo"]  
        usuario_info.expires_in = expires_in 
        usuario_info.save(update_fields=['token_acesso',
                                    'token_novo', 'expires_in'])
    else:
        usuario_info = Usuario_Spotify(usuario=session["usuario_id"], 
                                 token_acesso=session["token_acesso"],
                            token_novo=session["token_novo"], 
                            expires_in=expires_in)
        usuario_info.save()

    return usuario_info

# Essa função pega a ID do usuario que está pedindo acesso. Ela é importante pois é responsavel pelo relação usuario e equipe.
def pegar_user(token):
    base_url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + token}
    res = requests_call(url=base_url, method="GET", headers=headers)
    return res['id']

# Função de gerenciamento dos requests que cada função realiza. Sua criação foi feita para facilitar o controle e diminuir o uso de codigos repetidos.
def requests_call(method,url, user=None, headers=None, params=None, json=None):
    if user:
        user_info=Usuario_Spotify.objects.pegar_usuario(user=user)
        headers = {"Authorization": "Bearer " + user_info.pegar_token(),
                   "Content-Type": None}

    elif not headers:
        credentials = open_json()
        client_id= credentials["client_id"]
        client_secret= credentials["client_secret"]
        encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
        headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
        }
        if params['grant_type'] == 'authorization_code':
            params["redirect_uri"] = credentials["redirect_uri"]

    try:
        if method== "GET":
            response = requests.get(url=url,headers=headers,params=params)
        elif method == "POST":
            if not headers["Content-Type"]:
                headers["Content-Type"] = "application/json"
                response = requests.post(url=url,headers=headers,json=json)
            else:
                response = requests.post(url=url,headers=headers,params=params)
            
        response.raise_for_status()
        resJson = response.json()
    except requests.RequestException as e:
        print(e)
    else:
        return resJson
    
# Função que adiciona novas musicas a playlist.
def add_tracks_playlist(user,playlist_id, tracks):
    base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    data = {
        "uris": tracks
    }
    res = requests_call(user=user,method="POST",url=base_url, json=data)
    return res

# Função que pega a ID da playlist gerada.
def get_playlist(user,playlistId):
    base_url = f"https://api.spotify.com/v1/playlists/{playlistId}"
    query = {"fields" : 'external_urls'} 
    return requests_call(user=user,method="GET",url=base_url, params=query)

# Função que pega as musicas que estão presentes na playlist gerada.
def get_playlist_tracks(user, playlistId):
    base_url = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    data = {
        'fields': 'items(track(name,artists(name)))',
        'limit':30,
        'offset':0
    }
    return requests_call(user=user,method="GET",url=base_url, params=data)

# Função onde é pego as musicas recomendadas pelo spotify a partir do genero musical relacionado aos pokemons.
def get_recommendations(user,genres=None,tracks=None, limit=1, *args):

    base_url = "https://api.spotify.com/v1/recommendations/"
    
    seeds = dict(limit=limit)

    seeds["seed_artist"] =  None
    seeds["seed_genres"]= genres
    seeds["seed_tracks"]= None

    return requests_call(user=user,method="GET",url=base_url, params=seeds)

# Função que cria uma playlist nova na conta do usuario.
def create_playlist(user, nomePlaylist):

    base_url = "https://api.spotify.com/v1/users/"
    url = base_url + user + "/playlists"
    data = {
        "name": nomePlaylist,
        "description": "playlist generated from your pokemon team",
        "public": False
    }
    playlist_id  = requests_call(user=user,method="POST",url=url, json=data)

    return playlist_id['id']
