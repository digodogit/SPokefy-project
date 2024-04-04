from typing import Any
from django.db import models

#Classe para gerenciamento relacionados a Query. Ainda em desenvolvimento e aprendizado para utilização.
class EquipePkmnQuerySet(models.QuerySet):
    def equipe_atual(self):
        equipe = self.equipe_pkmn_set.all()
        print(equipe)
        pass

#classe para gerencionamento do models Usuario_Spotify. Ainda em desenvolvimento e aprendizado para utilização.
class SpotifyManager(models.Manager):
    def get_queryset(self):
        return EquipePkmnQuerySet(self.model, using=self._db)
    
    #Usado para devolver as informações do usuario, caso o usuario já tenha utilizado alguma vez.
    def pegar_usuario(self, user):
        usuario_info = Usuario_Spotify.objects.filter(usuario=user)

        if usuario_info.exists():
            return usuario_info[0]
        else:
            return None

#Models estruturado para ter tudo relacionado ao usuario do spotify, com os parametros necessarios para acessar o spotify API.
#Possui alguns métodos caracteristicos dos Models, mais um método de ajuda para retornar o token de acesso do spotify API e o nome de usuario da conta.
class Usuario_Spotify(models.Model):
    usuario = models.CharField(max_length=20, primary_key=True, unique=True,default='1')        # Usuario do spotify que está logado.
    token_acesso = models.CharField(max_length=150)                                             # Token de acesso ao spotify API.
    token_novo = models.CharField(max_length=150)                                               # O token usado para pedir renovação de token.
    data_token = models.DateTimeField(auto_now_add=True)                                        #
    expires_in = models.DateTimeField()                                                         # Quando tempo falta para expirar (uma hora)
    
    # Declarações para utilizar o gerenciamento e o Query.
    objects = SpotifyManager()
    equipes = SpotifyManager.from_queryset(EquipePkmnQuerySet)()

    # Checar se o token de acesso existe para esse usuario e retorna-lo.
    def pegar_token(self):
        if self.token_acesso:
            return self.token_acesso
        
    # Pegar o usuario logado.    
    def getuser(self) -> Any:
        return self.usuario
    

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("pokemon-page", kwargs= {
            'user': self.usuario
        })
    
    
    def __str__(self):
        return self.usuario
