# Fiap Embrapa API

## Enunciado
Você foi contratado(a) para uma consultoria e seu trabalho envolve analisar os dados de vitivinicultura da
Embrapa, os quais estão disponíveis aqui.
A ideia do projeto é a criação de uma API pública de consulta nos dados do site nas respectivas abas:

* Produção.
* Processamento.
* Comercialização.
* Importação.
* Exportação.

A API vai servir para alimentar uma base de dados que futuramente será usada para um modelo de Machine
Learning.

## Fase1: Requisitos
* Criar uma Rest API em Python que faça a consulta no site da Embrapa.
* Sua APl deve estar documentada.
* É recomendável (não obrigatório) a escolha de um método de autenticação (JWT, por exemplo).
* Criar um plano para fazer o deploy da API, desenhando a arquitetura do projeto desde a ingestão / até a alimentação do modelo (aqui não é necessário elaborar um modelo de ML, mas é preciso
que vocês escolham um cenário interessante em que a API possa ser utilizada).
* Fazer um MVP realizando o deploy com um link compartilhável e um repositório no github.

### Criar uma Rest API em Python que faça a consulta no site da Embrapa.
Foi criada uma API Flask expondo um endpoint para cada uma das abas. Devido â intermitência no site da Embrapa, os 
dados foram salvos localmente em formato CSV. Seu consumo e tratamento se dá em nível de código utilizando a biblioteca 
**Pandas**.

### Sua APl deve estar documentada.
A API foi documentada utilizando Swagger / OpenAPI via **Flask Smorest** (Blueprint). Para visualizá-la, execute
a aplicacão localmente e acesse a url **http://127.0.0.1:5000/swagger-ui**.

### É recomendável (não obrigatório) a escolha de um método de autenticação (JWT, por exemplo).
A autenticacão foi implementada **somente em nível de infraestrutura**, utilizando a estratégia de *client credentials* e
o recurso **Cognito**. Os testes e validaão podem ser feitos a partir da collection inclusa no json presente na pasta **/docs**.

### Criar um plano para fazer o deploy da API [...]
O diagrama solicitado encontra-se em formato **DrawIO** dentro da pasta **/docs**.

### Fazer um MVP realizando o deploy com um link compartilhável e um repositório no github.
Trata-se do material contigo neste repositório.
