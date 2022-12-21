# Desafio de detecção de retanguloes hachurados em uma imagem INDT

### Descrição do Desafio

Desenvolva uma aplicação que dada uma imagem com marcações (ver arquivos de exemplo) localize e informe:

    1. O número de marcações na primeira linha

    2. O número de marcações na primeira coluna

    3. O número de marcações na imagem

AS imagens para testes estão contidas na pasta ``images`` <br>
Ideia do algoritmo para esse desafio e essas caracteristicas de imagens.

Ok, vamos a explicação do passo passo como eu pensei nesse algoritmo, tentando ser o mais simples possível.

1. A primeira coisa que fiz foi colocar as imagens em preto e branco, elas já estão sim, mas por garantia prefiri fazer
   essa passagem novamente nesse filtros
2. Eu prefiri fazer um ``bitwise_not``, para inverter as cores da imagem, sendo onde é branco, se torna preto e
   vice-versa.
3. tendo a imagem dessa forma, eu consigo buscar todos os contornos da imagem , removendo o contorno mais externo de
   forma mais simples.
4. eu tendo os contornos consigo fazer mensuração de todos os contornos, ou seja, resolvo o passo 3 do desafio.
5. e eu também consigo fazer um slice para a primeira linha , consigo também a quantidade de hachuras na primeira linha,
   resolvendo o passo 1
6. Só que o mais complexo e mais importante é descobrir os valores da primeira coluna, para isso eu fiz os passos a
   seguir
4. ok, eu tenho os contornos, agora eu vou definir os centroides de cada retangulo com a função ``moments` e crio uma
   lista com todas as posições dos centroides
5. tendo os valores dos centroids, eu posso simplesmente ordenar os valores do eixo ``X`` de todos pontos e dessa forma
   consigo salvar numa váriavel esses valores minimos e saber quantos foram hachurados na primeira coluna

# Como usar o algoritmo

## Para executar é necessário rodar o seguinte comando

Para uma imagem apenas

``
python main.py --image images/4x14x187.bmp
``

Para uma pasta que contenham imagens do mesmo formato:

``
python main.py --folder images
``

Após a execução, será criada uma pasta chamada resultados, contendo um arquivo json para cada imagem

Cada resultado tem o seguinte nome ``4x14x187_resultado_leitura``

Se quiser ver o processo acontecendo e visualizar a imagem sendo processa é só adicionar o comando --view

Para uma imagem apenas

``
python main.py --image images/4x14x187.bmp --view true
``

Para uma pasta que contenham imagens do mesmo formato:

``
python main.py --folder images --view true
``

