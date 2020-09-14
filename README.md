# Web Scraping do Futebol Brasileiro

## Introdução

O meu objetivo neste repositório é reunir dados das conquistas dos principais times do futebol brasileiro (de acordo com a tabela do campeonato brasileiro de 2019) utilizando técnicas de web scraping e adicionar em um banco de dados central para que todos os interessados em análise do futebol possam usufruir.

Cada time também terá uma cópia local salva do arquivo HTML no momento em que foi acessado, para garantir que o código de web scraping continue funcionando caso haja atualização na página feita pelo clube.

Estarei acompanhando possíveis atualizações e atualizarei o código na medida do possível, para garantir os dados sempre atualizados.

Inicialemnte começarei com as conquistas de cada clube, mas nada impede de aumentar o escopo do projeto, expandindo por exemplo para dados sobre desempenho nos principais campeoanatos do Brasil.

A única regra que não será alterada é sobre o método de coleta dos dados. Utilizarei sempre web scraping para coleta.

Cada clube também terá uma análise feita por mim através do jupyter notebook, comparando por exemplo cada clube com o seu principal rival.

É muito trabalho pela frente, mas espero que os interessados pelo repositório fiquem satisfeitos e consigam realizar suas análise com os dados fornecidos.
  
## Lista dos clubes

Os times e respectivos status da coleta dos dados são listados a seguir:

|Clube|Status|
|---|---
|Athletico Paranaense |(in queue)|
|Atlético |(in queue)|
|Avaí |(in queue)|
|Bahia |(in queue)|
|Botafogo |(in queue)|
|Ceará |(in queue)|
|Chapecoense |(in progress)|
|Corinthians |(in queue)|
|Cruzeiro |(ok)|
|Csa |(in queue)|
|Flamengo |(in queue)|
|Fluminense |(in queue)|
|Fortaleza |(in queue)|
|Goiás |(in queue)|
|Grêmio |(ok)|
|Internacional |(ok)|
|Palmeiras |(in queue)|
|Santos |(in queue)|
|São Paulo |(in queue)|
|Vasco da Gama |(in queue)|

ok = Dados obtidos

in queue = Na fila para coleta de dados

in progress = Em andamento
