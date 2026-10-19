from .erros import ErroCadastro
from .partido import Partido
from .pessoas import Eleitor, Prefeito, Vereador
from .urna import Urna

class Eleicao:
    # cria as listas vazias da eleicao
    def __init__(self):
        self.partidos = []     
        self.eleitores = []    
        self.urnas = []
        self.erros = []         

    # coloca o partido na lista
    def inserir_partido(self, partido):
        self.partidos.append(partido)          

    # procura o partido pelo numero, se nao achar retorna None
    def buscar_partido(self, numero):
      
        for p in self.partidos:
            if p.numero == numero:
                return p

        return None
        

    # le o arquivo de partidos, se a linha der erro ela e ignorada
    def carregar_partidos(self, caminho):
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in arquivo:
                if not linha.startswith("PARTIDO:"):
                    continue                    
                tipo, resto = linha.split(":", 1)
                campos = resto.strip().split(",")
                
                try:
                    partido = Partido(int(campos[0]), campos[1], campos[2], campos[3])
                    self.inserir_partido(partido)
               
                except ErroCadastro as e:
                    self.erros.append(f"{e}: linha {campos}")

    # coloca o eleitor na lista
    def inserir_eleitor(self, eleitor):
        self.eleitores.append(eleitor)

    # le o arquivo de eleitores e cria eleitor, prefeito ou vereador
    def carregar_eleitores(self, caminho):
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in arquivo:
                if not linha.startswith(("ELEITOR:", "PREFEITO:", "VEREADOR:")):
                    continue
                tipo, resto = linha.split(":", 1)
                c = resto.strip().split(",")
                try:
                    if tipo == "ELEITOR":
                        pessoa = Eleitor(c[0], c[1], c[2], c[3], c[4], c[5])
                    elif tipo == "PREFEITO":
                        partido = self.buscar_partido(int(c[7]))
            
                        pessoa = Prefeito(c[0], c[1], c[2], c[3], c[4], c[5], c[6], partido, c[8], c[9])
                    else:
                        
                        partido = self.buscar_partido(int(c[7]))
                        pessoa = Vereador(c[0], c[1], c[2], c[3], c[4], c[5], c[6], partido, c[8], c[9])
                    
                    self.inserir_eleitor(pessoa)
                except ErroCadastro as e:
                    self.erros.append(f"{e}: linha {c}")

    # coloca a urna na lista
    def inserir_urna(self, urna):
        self.urnas.append(urna)

    # procura a urna pela zona e secao, se nao achar retorna None
    def buscar_urna(self, zona, secao):
        for p in self.urnas:
            if p.zona == zona and p.secao == secao:
                return p
            
        return None
        

    # le o arquivo de votos e coloca cada voto na urna certa
    def carregar_urnas(self, caminho):
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in arquivo:
                if not linha.startswith("VOTO:"):
                    continue
                tipo, resto = linha.split(":", 1)
                c = resto.strip().split(",")
                zona = int(c[0])
                secao = int(c[1])
                urna = self.buscar_urna(zona, secao)
                if urna is None:
                    urna = Urna(zona, secao)
                    self.inserir_urna(urna)
                urna.registrar_voto(c[3], c[4])

    # faz o relatorio de eleitores
    def relatorio_eleitores(self, caminho):
        linha = "-" * 40
        prefeitos = 0
        vereadores = 0
        zonas = {}                                   # {zona: {secao: quantidade}}
        for e in self.eleitores:
            if isinstance(e, Prefeito):
                prefeitos += 1
            elif isinstance(e, Vereador):
                vereadores += 1
            if e.zona not in zonas:
                zonas[e.zona] = {}
            zonas[e.zona][e.secao] = zonas[e.zona].get(e.secao, 0) + 1

        with open(caminho, "w", encoding="utf-8") as arq:
            arq.write(f"{linha}\nRelatorio de Eleitores\n{linha}\n")
            arq.write(f"Eleitores: {len(self.eleitores)}\n")
            arq.write(f"Candidatos a prefeito: {prefeitos}\n")
            arq.write(f"Candidatos a vereador: {vereadores}\n")
            for zona in sorted(zonas):
                arq.write(f"\nZona {zona}:\n")
                for secao in sorted(zonas[zona]):
                    arq.write(f" - Seção {secao}: {zonas[zona][secao]} eleitores\n")
            arq.write(f"{linha}\n\n")

    # faz o relatorio de partidos
    def relatorio_partidos(self, caminho):
        linha = "-" * 40
        with open(caminho, "w", encoding="utf-8") as arq:
            arq.write(f"{linha}\n")
            arq.write("Relatorio de Partidos\n")
            arq.write(f"{linha}\n")
            arq.write(f"Total de partidos: {len(self.partidos)}\n")

            for p in self.partidos:
                prefeitos_candidatos = 0
                vereadores_candidatos = 0
                for e in self.eleitores:
                    if isinstance(e, Prefeito) and e.partido is p:
                        prefeitos_candidatos += 1
                    if isinstance(e, Vereador) and e.partido is p:
                        vereadores_candidatos += 1
                arq.write(f"\n{p.nome} ({p.sigla}):\n")
                arq.write(f" - Prefeitos candidatos: {prefeitos_candidatos}\n")
                arq.write(f" - Vereadores candidatos: {vereadores_candidatos}\n")

            arq.write(f"{linha}\n\n")

    # pega os numeros dos candidatos de um tipo (prefeito ou vereador)
    def numeros_candidatos(self, classe):
        numeros = []
        for e in self.eleitores:
            if isinstance(e, classe):
                numeros.append(str(e.numero))
        return numeros

    # conta os votos validos, brancos e nulos
    def apurar(self, votos, numeros_validos):
        validos = brancos = nulos = 0
        for numero, qtd in votos.items():
            if numero == "":
                brancos += qtd
            elif numero in numeros_validos:
                validos += qtd
            else:
                nulos += qtd
        return validos, brancos, nulos

    # faz o relatorio de cada urna
    def relatorio_urnas(self, caminho):
        linha = "-" * 40
        numeros_prefeito = self.numeros_candidatos(Prefeito)
        numeros_vereador = self.numeros_candidatos(Vereador)
        with open(caminho, "w", encoding="utf-8") as arq:
            for urna in self.urnas:
                vp, bp, np = self.apurar(urna.votos_prefeito, numeros_prefeito)
                vv, bv, nv = self.apurar(urna.votos_vereador, numeros_vereador)
                arq.write(f"{linha}\n")
                arq.write(f"Relatorio da Urna - Zona {urna.zona} - Seção {urna.secao}\n")
                arq.write(f"{linha}\n")
                arq.write(f"Votos validos para prefeito: {vp}\n")
                arq.write(f"Votos brancos para prefeito: {bp}\n")
                arq.write(f"Votos nulos para prefeito: {np}\n")
                arq.write(f"Votos validos para vereador: {vv}\n")
                arq.write(f"Votos brancos para vereador: {bv}\n")
                arq.write(f"Votos nulos para vereador: {nv}\n")
                arq.write(f"{linha}\n\n")

    # faz o relatorio geral, soma as urnas e ve quem ganhou
    def relatorio_geral(self, caminho):
        linha = "-" * 40

        total = self.urnas[0]
        for urna in self.urnas[1:]:
            total = total + urna

        votos_validos = 0
        vencedor = None
        votos_vencedor = 0
        for e in self.eleitores:
            if isinstance(e, Prefeito):
                votos = total.votos_prefeito.get(str(e.numero), 0)
                votos_validos += votos
                if votos > votos_vencedor:
                    vencedor = e
                    votos_vencedor = votos

        if vencedor is not None and votos_vencedor >= votos_validos / 2:
            resultado = vencedor.nome
        else:
            resultado = "Segundo Turno"

        ranking = []
        for e in self.eleitores:
            if isinstance(e, Vereador):
                ranking.append((e, total.votos_vereador.get(str(e.numero), 0)))
        ranking = sorted(ranking, key=lambda item: item[1], reverse=True)

        with open(caminho, "w", encoding="utf-8") as arq:
            arq.write(f"{linha}\n")
            arq.write("Relatorio Geral da Eleicao\n")
            arq.write(f"{linha}\n")
            arq.write(f"Prefeito eleito: {resultado}\n")
            arq.write("Vereadores eleitos:\n")
            for vereador, votos in ranking[:10]:
                arq.write(f" - {vereador.nome}: {votos} votos\n")
            arq.write(f"{linha}\n")

    # faz o relatorio de erros
    def relatorio_erros(self, caminho):
        linha = "-" * 40
        with open(caminho, "w", encoding="utf-8") as arq:
            for msg in self.erros:
                arq.write(f"{msg}\n")
            arq.write(f"{linha}\n")
            arq.write("Relatorio de Erros\n")
            arq.write(f"{linha}\n")
            arq.write(f"Partidos com nome ou CNPJ inválido: {Partido.erros_validacao}\n")
            arq.write(f"Candidatos a prefeito com número inválido: {Prefeito.erros_numero}\n")
            arq.write(f"Candidatos a vereador com número inválido: {Vereador.erros_numero}\n")
            arq.write(f"{linha}\n\n")