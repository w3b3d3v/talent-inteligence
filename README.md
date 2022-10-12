# Talent-inteligence

## Link de entrada do bot

https://discord.com/api/oauth2/authorize?client_id=977251314641801226&permissions=121333443648&scope=bot

# Named Entity Recognition

O modelo de reconhecimento de entidades nomeadas é um modelo de processamento de linguagem natural ou NLP, que busca reconhecer e nomear entidades de um texto.

Por exemplo, na frase: Meu nome é Lorenzo, moro no Rio Grande do Sul e tenho um celular da Apple.

O modelo deve reconhecer Lorenzo como nome, Rio Grande do Sul como localização e Apple como uma empresa, uma marca.

## Mas como utilizaremos isso na web3dev?

Isso será utilizado no aproveitamento do canal do discord #apresente-se , permitindo a captação de dados dos usuários, e posterior uso em outros projetos. Para exemplificar, vamos pensar na seguinte situação: 

- Uma empresa contata a web3dev buscando desenvolvedores para determinada tecnologia, digamos que Ruby On Rails.
- A web3dev possui alguns desenvolvedores mais próximos como contato, mas não sabe especificamente quais tem especialidade em Ruby.
- E agora? Como atingir os desenvolvedores Ruby?

Nessa situação, a utilização do modelo de reconhecimento de entidade permitiria encontrar de maneira orgânica os desenvolvedores Ruby e atingi-los diretamente na divulgação da vaga. Isso permitiria um recrutamento melhor e um melhor mapeamento das especializações da nossa comunidade.

Além disso, esse modelo pode ser utilizado para analisar os dados da nossa comunidade, como tecnologias mais comuns, maior quantidade de desenvolvedores… Enfim, desenvolver pesquisa em cima desses dados.

## Qual a Stack, tecnologias utilizadas?

Essa tecnologia será construída por meio de um discord bot. Esse bot, para uma versão MVP que foi desenvolvida em 3 semanas, foi construída por meio da linguagem JavaScript. Entretanto, uma migração para a API Python é muito interessante, já que o modelo é escrito em Python, então a integração será feita de maneira mais fácil.

No modelo atual, o discord bot recebe um comando com o ID do canal que ele deve buscar as mensagens. Depois, ele armazenas as mensagens em um banco de dados para processamento posterior.

O modelo é construído com Python, utilizando a biblioteca Spacy. Essa biblioteca permite a criação de modelos facilitados (visto que já tinha a base para um NER).

Os dados de treinamento foram retirados de canais de apresentação de diferentes servidores do Discord relacionados a tecnologia. Esses dados foram anotados por mim, manualmente. Hoje, o modelo é treinado com apenas 100 exemplos anotados, ou seja, é um modelo de aprendizado supervisionado. Isso significa que o modelo treina a partir do dataset anotado de treinamento, é punido por erros e gradativamente aprende a relacionar cada entidade com o texto. É um modelo de rede neural.

A utilização de 100 exemplos apenas pode afetar o desempenho do modelo, visto que uma maior quantidade de exemplos (a combinar) podem significar em um modelo mais generalista e mais preciso. 

Porém, a anotação de cada categoria de palavra precisa ser feita manualmente através de um app chamado label-studio.

## Funcionamento do modelo

As explicações a seguir serão baseadas na explicação oficial da documentação spacy, apontada nesse artigo: [https://explosion.ai/blog/deep-learning-formula-nlp](https://explosion.ai/blog/deep-learning-formula-nlp)

Os modelos de processamento de linguagem natural da spacy utilizam uma fórmula, conhecida como: Embed, Encode, attend, predict, que são etapas do processamento de um modelo.

Representações embutidas de palavras, conhecidas como vetores de palavras é uma das tecnologias mais usadas no campo de processamento de linguagens, visto que permitem tratar palavras como unidades relativas de significado, ao invés de coisas distintas. 

### Passo 1: Embed

Uma tabela de embedding mapeia vetores binários longos e espalhados em vetores contínuos, menores e mais densos. Por exemplo, se recebêssemos nosso texto em uma sequência ASCII de caracteres, existem 256 possibilidades de valor, e representamos isso em um vetor binário de 256 dimensões. Isso é chamado de one hot encoding. Valores diferentes recebem vetores inteiramente diferentes.

A maioria das redes neurais tokenizam o texto em palavras e depois fazem o embedding das palavras em vetores.

### Passo 2: Encode

Dada uma sequência de vetores de palvras, esse passo computa uma representação do que chamamos uma matriz de sentença, onde cada linha representa o significado de cada token no contexto da frase.

A tecnologia usada aqui é o bidirecitonal RNN. O vetor de cada token é computado em duas partes, uma com um passo para frente, e outra com um passo para trás. Depois, juntamos os dois para ter o vetor completo.

É basicamente a computação de uma representação intermediária, representando os tokens dentro de um contexto. Assim, o modelo saberá diferenciar expressões pelo contexto. 

### Passo 3: Attend

Esse passo reduz a representação de matriz produzida pelo passo anterior para um único vetor, pois dessa maneira ele pode ser passado para uma rede feed-forward para a predição. 

### Passo 4: Predict

Uma vez que os textos foram reduzidos para um único vetor, podemos aprender a representação que queremos, no nosso caso, um label de classe.
