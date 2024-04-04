import requests
import json
from .models import Equipe_Pkmn
from django.http import HttpResponse


# Operations são funções e classes usados para auxiliar o que está sendo usado no Views.
# É uma forma de deixar mais limpo o código para melhor gerenciamento e entendimento do que está sendo feito.

# Função de exceção para caso um pokemon não possa ser adicionado. Atualmente não sendo usada.
def pkmnerror(Exception):
    print(Exception)
    return Exception

# Classe de auxilio na criação de um pokemon que vem do PokeAPI. 
# Usada para ter melhor controle do pokemon em si, antes de ser passado ao Model Equipe_Pkmn e ser adicionado ao banco de dados.
class Pkmn(object):
    def __init__(self, nome):
        self.nome = nome                                # Nome do pokemon
        self.err = None                                 # Caso haja algum erro na criação dele.
        self.genero, self.sprite = self.add_tipo()      # Vinculação do genero e a sprite do pokemon. São feitas pelo returno da função add_tipo.

    # Adiciona o tipo e o sprite do pokemon em questão. Retorna erro caso não seja possivel criar o pokemon.
    def add_tipo(self):
        genero, sprite, err = api_poke(self.nome, self.err)
        if err:
            self.err = err
            return None
        else:
            return genero, sprite
    
    def __str__(self):
        return str(self.nome)

# Função que acessa o PokeAPI para criar o pokemon que será adicionado na equipe.
def api_poke(pkmn, err):
    pkmn_genero = []
    poke_img=''
    try:
        res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pkmn}/')
        res.raise_for_status()
    except requests.RequestException: 
        err = res.status_code

    else:
        # Os tipos existentes no universo Pokemon são relacionados a generos musicais por mim.
        # Essa relação e a a "cor" utilizada para representar o tipos/generos estão em um Json. Que é aberto e atrelado a variavel "arquivoJ".
        api_data = res.json()
        arquivoJ = open_json()

        # Como cada pokemon pode ter 2 tipos, sse primeiro "for" separa o "type" do pokemon vindo do PokeAPI e adiciona a um vetor o "genero" e a "cor".
        for tipo in api_data['types']:
            poke_tipo = tipo['type']['name']
            pkmn_genero.append(arquivoJ["pkmntypes"][poke_tipo])
        
        # Já esse "for" é usado para pegar o sprite ao pokemon.
        for img, value in api_data['sprites'].items():
            if img =="front_default" and value:
                poke_img = value

    return pkmn_genero, poke_img, err

# Função de abertura de arquivo json.
def open_json():
        with open('relations.json', 'r') as file:
            return json.load(file)

# Função que adiciona o pokemon a equipe pokemon do usuario. Usando o método presente no método "Equipe_Pkmn".
def adicionar_pkmn_na_equipe(equipe_atual, pkmn):
    return Equipe_Pkmn.add_pkmn(self=equipe_atual, pkmn=pkmn.nome, genero=pkmn.genero, sprite=pkmn.sprite)
