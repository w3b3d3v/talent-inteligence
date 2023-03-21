# Talent-inteligence - Web3dev

O Talent-inteligence é o caçador de talentos da nossa web3dev! 

O Talent Intelligence é um bot para Discord que tem como objetivo ajudar as empresas a encontrar talentos promissores e armazená-los em um banco de dados para futuras contratações. O bot utiliza a API da OpenAI para extrair informações valiosas a partir das mensagens de apresentação dos usuários que se apresentaram no discord.

Além de ser um excelente recurso para recrutamento, o Talent Intelligence também oferece recursos de moderação para ajudar os moderadores do servidor a gerenciar e manter a comunidade. Com suas capacidades de análise e categorização, o bot pode identificar categorias de trabalho e tecnologia, além de nomear automaticamente as mensagens de apresentação dos usuários.

O projeto foi desenvolvido em Python, tornando-o acessível para programadores de todos os níveis de habilidade. A API da OpenAI é usada para fornecer uma análise detalhada das mensagens de apresentação, permitindo que o bot identifique facilmente informações relevantes para os recrutadores.

## Link de entrada do bot

https://discord.com/api/oauth2/authorize?client_id=977251314641801226&permissions=121333443648&scope=bot

## Contribuindo 

Para contribuir com o talent-intelligence, sinta-se livre para criar Issues no projeto com sugestões de melhora, bugs, ou ideias de novas features. Se quiser, coloque a mão na massa e desenvolva em cima do projeto. Basta fazer um fork do repositório, criar uma aplicação [aqui](https://discord.com/developers/applications) e bora pro código!

Para rodar o código, crie um ambiente virtual em python:

`python3 -m venv venv`
`source venv/bin/activate`

Para quem estiver em um sistema operacional diferente de Linux: https://docs.python.org/3/library/venv.html

Agora, vamos instalar as dependências:

`pip3 install -r requirements.txt`

E pronto, seu projeto está pronto para rodar! Agora configure sua chave de API da OpenaAI [aqui](https://platform.openai.com/docs/api-reference) e adicione a um arquivo `.env` na raíz do repositório com as variáveis demonstradas no arquivo `.env.example`. Você precisa das chaves do Discord e da OpenAI

Para incializar o bot, rode: 
`python3 bot.py`

E pronto! Agora é só desenvolver e abrir um Pull Request no repositório, para que nós possamos revisar e quem sabe integrar sua alteração ao bot!
