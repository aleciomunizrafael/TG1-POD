class Urna:
    # cria a urna com zona, secao e os votos vazios
    def __init__(self, zona, secao):
        self.zona = zona
        self.secao = secao
        self.votos_prefeito = {}     # dicionário: número votado → quantidade
        self.votos_vereador = {}

    # coloca mais um voto pro numero no cargo certo
    def registrar_voto(self, cargo, numero):
    
        if cargo == "PREFEITO":
                self.votos_prefeito[numero] = self.votos_prefeito.get(numero, 0) + 1
        else:
            self.votos_vereador[numero] = self.votos_vereador.get(numero, 0) + 1

    # soma duas urnas, a nova fica com zona e secao None
    def __add__(self, outra):
        if not isinstance(outra, Urna):
            return NotImplemented
        nova = Urna(None, None)
        
        for urna in (self, outra):                          
            for numero, qtd in urna.votos_prefeito.items(): 
                nova.votos_prefeito[numero] = nova.votos_prefeito.get(numero, 0) + qtd
                          
            for numero, qtd in urna.votos_vereador.items(): 
                nova.votos_vereador[numero] = nova.votos_vereador.get(numero, 0) + qtd
                
        return nova 