from django.db import models
from spokefyapp.models import Usuario_Spotify


#Classe para gerenciamento relacionados a Query. Ainda em desenvolvimento e aprendizado para utilização.
class EquipePkmnQuerySet(models.QuerySet):
    def equipe_atual(self, usuario, nome_equipe):
        pass
    def user (self):
        pass

#classe para gerencionamento do models Equipe_Pkmn. Ainda em desenvolvimento e aprendizado para utilização.
class EquipePkmnManager(models.Manager):
    def get_queryset(self):
        return EquipePkmnQuerySet(self.model, using=self._db)


#Models estruturado para ter tudo relacionado a equipe pokemon do usuario e a playlist que foi gerada a partir dela.
#Possui alguns métodos caracteristicos dos Models, mais 3 métodos de apoio para registro e exclusão correta do pokemon com a equipe.
class Equipe_Pkmn(models.Model):

    usuario = models.ForeignKey(Usuario_Spotify, on_delete=models.CASCADE)      # Relaciona o usuario do spotify com a equipe sendo criada.
    nome_equipe = models.CharField(max_length=20)                               # nome da equipe a ser criada.
    tamanho_equipe = models.IntegerField(default=0)                             # tamanho da equipe atual com max de 6 pokemons.
    pkmn_list = models.JSONField(default=dict)                                  # A lista dos pokemons que foram adicionados a equipe.
    playlist = models.CharField(max_length=20, default=None, null=True)         # a ID da Playlist que foi gerada a partir da equipe.
    
    # Declarações para utilizar o gerenciamento e o Query.
    objects= EquipePkmnManager()
    get_user = EquipePkmnManager.from_queryset(EquipePkmnManager)()
    
    #adiciona o pokemon ao models e retorna o objeto inteiro.
    def add_pkmn(self, pkmn, genero,sprite=None):
   
        self.pkmn_list[pkmn]={
            'atributos': genero,
            'sprite': sprite
        
        }
        self.tamanho_equipe +=1
        self.save()
        return self
    
    #deleta o pokemon do models.
    def del_pkmn(self, pkmn):
        self.pkmn_list.pop(pkmn)

        self.tamanho_equipe-=1
        self.save()
        return print("excluido")
    
    #separa os atributos salvos tirando a "cor" e deixando apenas o "genero musical" relacionado ao pokemon e seu tipo.
    def get_genero(self):
        generos =[]
        for atributo in self.pkmn_list.values():
            for x, iters in enumerate(atributo["atributos"]):
                iters.pop("cor") 
                
            generos+=atributo["atributos"]
        
        return generos
            
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("criar-pkmn", kwargs={ 'user': str(self.usuario),
            'nome_equipe': self.nome_equipe,})
    
    def __str__(self):
        return self.nome_equipe + ' ' + str(self.pkmn_list)  