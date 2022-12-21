# Desafio de detecção de retângulos hachurados em uma imagem INDT

### Descrição do Desafio

Desenvolva uma aplicação que dada uma imagem com marcações (ver arquivos de exemplo) localize e informe:

    1. O número de marcações na primeira linha

    2. O número de marcações na primeira coluna

    3. O número de marcações na imagem


### Processo de desenvolvimento

As imagens para testes estão contidas na pasta ``images``

Ideia do algoritmo para esse desafio e essas caracteristicas de imagens.

Ok, vamos a explicação do passo a passo como eu pensei nesse algoritmo, tentando ser o mais simples possível.

1. A primeira coisa que fiz foi ler a imagem e já colocar em escalas de cinza;
2. Usando a imagem em escala de cinza utilizei ``bitwise_not``, para inverter as cores da imagem, sendo onde é branco,
   se torna preto e
   vice-versa;
3. tendo a imagem dessa forma, eu consigo buscar todos os contornos da imagem, removendo o contorno mais externo de
   forma mais simples;
4. Agora eu busco todos os contornos, e limito clado na altura, largura e area, para que eu tenha apenas as hachuras;
5. Ok, eu tenho os contornos, agora eu vou definir os centroides de cada retangulo com a função ``moments` e crio uma
   lista com todas as posições dos centroides das hachuras;
6. Com os centroides eu consigo mensurar os valores da primeira linha e também da primeira coluna
7. E usando a mesma ideia, eu tenho também os contornos totais, terminando assim o processo solicitado no desafio.

### Melhorias que eu faria se eu tivesse mais tempo

1. Eu enxergo que a solução que fiz ela é limitada, pois se eu precisar fazer buscas mais complexas, isso se tornará um
   problema;
2. O que eu faria com mais tempo de desenvolvimento, eu criaria uma mapa para o papel que eu preciso ler, essa ideia eu
   retiro de um projeto que acompanho há 4 anos;
3. O link do projeto é https://github.com/Udayraj123/OMRChecker;
4. Como a leitura de testes de vestibular da India é bem caótica, e um volante de loteria também pode ser, criar um
   sistema que possa receber um mapa e já se atualizar automaticamente é uma saída que pode ser interessante ao invés de
   fixar o mapa no código.

# Como usar o algoritmo

## Para executar é necessário rodar o seguinte comando

É interessante criar um virtualenv para rodar o projeto.

[Virtualenv](https://docs.python.org/3/library/venv.html)

Para instalar as depedências

``
python -m pip install -r requirements.txt
``

Para uma imagem apenas

``
python main.py --image images/4x14x187.bmp
``

Para uma pasta que contenham imagens do mesmo formato:

``
python main.py --folder images
``

Após a execução, será criada uma pasta chamada ``resultados``, contendo um arquivo json para cada imagem

Cada resultado tem o seguinte nome ``4x14x187_resultado_leitura``

Se quiser ver o processo acontecendo e visualizar a imagem sendo processa é só adicionar o comando ``--view true``

Para uma imagem apenas

``
python main.py --image images/4x14x187.bmp --view true
``

Para uma pasta que contenham imagens do mesmo formato:

``
python main.py --folder images --view true
``


## Algumas definições de software que tomei


Decidi criar uma classe que contenha todos os metodos para os processos funcionarem de formas mais isoladas.
Para que o algorimo seja funcional, há um metodo apenas para execução que é o ``run`` dai em diante todo o processo é feito automaticamente.
