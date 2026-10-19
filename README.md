# TG1 - Sistema de Votação

Programa que simula uma eleição para prefeito e vereador.

## Como rodar

```
python3 app.py Partidos.txt Eleitores.txt Urnas.txt
```

Exemplo:

```
python3 app.py Input/caso1/Partidos.txt Input/caso1/Eleitores.txt Input/caso1/Urnas.txt
```

Os relatórios são salvos na pasta `output`.

## Arquivos

- `app.py`: programa principal
- `eleicao/`: pacote com as classes do trabalho
- `Input/`: arquivos de entrada
- `output/`: relatórios gerados

## Usando o pacote

```python
from eleicao.eleicao import Eleicao

eleicao = Eleicao()
eleicao.carregar_partidos("Input/caso0/Partidos.txt")
eleicao.carregar_eleitores("Input/caso0/Eleitores.txt")
eleicao.carregar_urnas("Input/caso0/Urnas.txt")
eleicao.relatorio_geral("output/geral.out")
```
