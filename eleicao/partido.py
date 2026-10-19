from .erros import ErroCadastro

class Partido:
    erros_validacao = 0 
    # construtor do partido, se o nome ou o cnpj der erro conta mais um erro
    def __init__(self, numero, sigla, nome, cnpj):
        self.numero = numero
        self.sigla = sigla
        try:
            self.nome = nome
            self.cnpj = cnpj
        except ErroCadastro:
            Partido.registrar_erro()
            raise

    # soma 1 no contador de erros do partido
    @classmethod
    def registrar_erro(cls):
        cls.erros_validacao += 1 
    

    # getter do cnpj
    @property
    def cnpj(self):
        return self._cnpj

    # setter do cnpj, tem que ter 14 numeros
    @cnpj.setter
    def cnpj(self, valor):
        if len(valor) != 14 or not valor.isdigit():
            raise ErroCadastro ("Partido", "cnpj", valor)
        self._cnpj = valor
    
    # getter do nome
    @property
    def nome(self):               
        return self._nome

    # setter do nome, nao pode passar de 50 letras
    @nome.setter
    def nome(self, valor):        
        if len(valor) > 50:
            raise ErroCadastro("Partido", "nome", valor)
        self._nome = valor