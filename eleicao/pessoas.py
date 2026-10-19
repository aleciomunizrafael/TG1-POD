from .erros import ErroCadastro
from abc import ABC, abstractmethod

class Eleitor:
    # construtor do eleitor, zona e secao viram int
    def __init__(self, nome, cpf, nascimento, titulo, zona, secao):
        self.nascimento = nascimento
        self.titulo = titulo
        self.zona = int(zona)
        self.secao = int(secao)
        self.nome = nome
        self.cpf = cpf

        
    # getter do nome
    @property
    def nome(self):
        return self._nome

    # setter do nome, nao pode passar de 50 letras
    @nome.setter
    def nome(self, valor):
        if len(valor) > 50:
            raise ErroCadastro (type(self).__name__, "nome", valor)
        self._nome = valor
    
    # getter do cpf
    @property
    def cpf(self):               
        return self._cpf

    # setter do cpf, tem que ter 11 numeros
    @cpf.setter
    def cpf(self, valor):        
        if len(valor) != 11 or not valor.isdigit():
            raise ErroCadastro(type(self).__name__, "cpf", valor)
        self._cpf = valor

class Candidato(Eleitor, ABC):
    # construtor do candidato, usa o do eleitor e depois confere o numero
    def __init__(self, nome, cpf, nascimento, titulo, zona, secao, numero, partido):
        super().__init__(nome, cpf, nascimento, titulo, zona, secao)   
        if not self.validar_numero(numero):
            self.registrar_erro()          
            raise ErroCadastro(type(self).__name__, "numero", numero)
        self.numero = int(numero)
        self.partido = partido

    # metodo abstrato, o prefeito e o vereador que fazem ele
    @abstractmethod
    def validar_numero(self, numero):
        pass
        
class Prefeito(Candidato):
    erros_numero = 0       

    # construtor do prefeito, tambem confere o cpf do vice
    def __init__(self, nome, cpf, nascimento, titulo, zona, secao, numero, partido,
                cpf_vice, plano_governo):
        super().__init__(nome, cpf, nascimento, titulo, zona, secao, numero, partido)
        self.plano_governo = plano_governo
        if len(cpf_vice) != 11 or not cpf_vice.isdigit():
            raise ErroCadastro(type(self).__name__, "cpf_vice", cpf_vice)
        self.cpf_vice = cpf_vice

    # numero do prefeito tem que ter 2 digitos
    def validar_numero(self, numero):
        if len(numero) == 2 and numero.isdigit():
            return True
        return False
            

    # soma 1 nos erros de numero do prefeito
    @classmethod
    def registrar_erro(cls):
        cls.erros_numero += 1

class Vereador(Candidato):
    erros_numero = 0       

    # construtor do vereador
    def __init__(self, nome, cpf, nascimento, titulo, zona, secao, numero, partido, bairro, projeto_lei):
        super().__init__(nome, cpf, nascimento, titulo, zona, secao, numero, partido)
        self.bairro = bairro
        self.projeto_lei = projeto_lei
        

    # numero do vereador tem que ter 5 digitos
    def validar_numero(self, numero):
        if len(numero) == 5 and numero.isdigit():
            return True
        return False
            

    # soma 1 nos erros de numero do vereador
    @classmethod
    def registrar_erro(cls):
        cls.erros_numero += 1

    