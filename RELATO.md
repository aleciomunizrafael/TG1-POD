# Relato - TG1

## Divisão do trabalho

Fiz o trabalho sozinho, então fiquei responsável por todas as partes: as classes, a leitura dos arquivos, os relatórios, o README e este relato.

## Desenvolvimento

Fui construindo o sistema por partes, nesta ordem: a exceção 'ErroCadastro', a classe 'Partido', o 'Eleitor' e os candidatos ('Candidato', 'Prefeito' e 'Vereador'), a 'Urna', a classe 'Eleicao' com a leitura dos arquivos, os relatórios e, por último, o 'app.py'. Depois de terminar cada classe, eu testava ela num arquivo separado antes de passar para a próxima. No final, comparei os relatórios gerados com os gabaritos do caso0 e do caso1.

## Dificuldades

Como eu era mais acostumado em Java, uma das dificuldades foi me acostumar com o Python. No começo eu confundia o 'try' e o 'except' e tentei usar o 'except' como se fosse um 'else', sem entender que ele só roda quando acontece um erro. Também tentei usar o '++' do Java, e tive que trocar por '+= 1'.

Outras dificuldades foram:

- No setter, eu validava 'self.cpf' em vez do 'valor' recebido, o que dava erro porque o atributo ainda não existia. Também precisei entender por que o valor fica guardado em 'self._cpf', com '_' na frente.
- As linhas de candidato no arquivo de eleitores tinham dois campos a mais (número e partido) do que o cabeçalho do arquivo mostrava.
- Na hora de achar a urna, o texto "1" é diferente do número 1, então precisei converter a zona e a seção com 'int()'.
- Quando eu abria o arquivo com 'open(..., "w")' dentro do 'for', ele apagava tudo o que já tinha sido escrito, e só sobrava a última parte.

## Evolução

Com este trabalho aprendi:

- herança e classe abstrata em Python;
- '@property' e setters para validar os dados;
- sobrecarga de operadores, com o '__add__' para somar as urnas.
