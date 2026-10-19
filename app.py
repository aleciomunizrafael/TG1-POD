import sys
from eleicao.eleicao import Eleicao


# programa principal, le os arquivos e gera os relatorios
def main():
    if len(sys.argv) != 4:
        print("Uso: python app.py Partidos.txt Eleitores.txt Urnas.txt")
        sys.exit(1)

    arq_partidos, arq_eleitores, arq_urnas = sys.argv[1], sys.argv[2], sys.argv[3]

    eleicao = Eleicao()
    try:
        eleicao.carregar_partidos(arq_partidos)
        eleicao.carregar_eleitores(arq_eleitores)
        eleicao.carregar_urnas(arq_urnas)
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e.filename}")
        sys.exit(1)

    eleicao.relatorio_eleitores("output/eleitores.out")
    eleicao.relatorio_partidos("output/partidos.out")
    eleicao.relatorio_urnas("output/urnas.out")
    eleicao.relatorio_geral("output/geral.out")
    eleicao.relatorio_erros("output/erros.out")
    print("Relatórios gerados na pasta output/")


if __name__ == "__main__":
    main()