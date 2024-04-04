from . import views
from django.urls import path, re_path
from spokefyapp.views import criar_playlist as viewspotify

urlpatterns = [
    path("<user>/pokemon/", views.home_page, name="pokemon-page"),
    path("<user>/pokemon/criar/", views.criar_equipe_pkmn, name="criar_equipe_pkmn"),
    path("<str:user>/pokemon/<str:nome_equipe>/playlist/", viewspotify, name="criar-playlist"),
    path("<str:user>/pokemon/<str:nome_equipe>/adicionar/", views.criar_pkmn, name="criar-pkmn"),
    path("<str:user>/pokemon/<str:nome_equipe>", views.editar_equipe_pkmn, name="editar-equipe-pkmn"),
    path("<str:user>/pokemon/<str:nome_equipe>/excluir/", views.excluir_equipe_pkmn, name="excluir-equipe-pkmn"),
    path("<str:user>/pokemon/<str:nome_equipe>/excluir/<str:nome_pkmn>", views.excluir_pkmn, name="excluir-pkmn"),
    path("<str:user>/pokemon/<str:nome_equipe>/playlist=<str:playlist_id>", views.display_playlist, name="display-playlist")
    #re_path(r'^(?P<user>[^/]+)/(?P<kwargs>[^/]+)$', viewspotify, name="criar-playlist"),
]