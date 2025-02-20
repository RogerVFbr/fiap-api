# News Recommenaation System: Inference API
Este repositório contém a implementação de uma API para inferência de um modelo de recomendação de notícias.

---

## Índice
- [Abordagem](#abordagem)
- [Docker](#docker)
- [Testes](#testes)
- [Deploy](#deploy)
- [Infraestrutura](#infraestrutura)
- [Contrato](#Contrato)

---

## Abordagem
A API foi desenvolvida utilizando uma aplicação Python Flask containerizada rodando dentro de uma função Lambda,
dentro do preceito serverless de publicação. Esta abordagem possui a vantagem de ser escalável e de baixo custo,
porém com limitações fundamentais para ambientes produtivos devido ao seu amplo tempo de cold start. Ainda assim
se fez uma escolha consciente para fins de demonstração.

## Docker
O código e suas dependências foram encapsuladas em um container Docker que é construido e publicado em tempo de
esteira no AWS Elastic Container Registry.

## Testes
Para testes deve-se utilizar a collection do Insomnia disponível no arquivo `Insomnia_2025-02-20.json` (pasta **docs**). Esta collection
facilitará o processo de autenticação, buscando automaticamente o token de acesso nos endpoints do Incognito. Baixe e
instale uma instância do Insomnia e importe a collection conforme instruções do fabricante para começar a testar a API.

Também é possível executar a api localmente conforme procedimento padrão do Flask após a instalação das dependências e 
registro das credenciais AWS fornecidas.

## Deploy
O deploy da API é feito automaticamente via Github Actions, que publica a imagem Docker no ECR e atualiza a função Lambda.

## Infraestrutura
A infraestrutura é gerenciada via Terraform e consiste em uma função Lambda, um API Gateway e configurações auxiliares.

---

## Contrato

### 1. Warm-up

**`GET /warmup`**  
Verifica o estado da API.

**Resposta:**
- `200 OK`: API está ativa.
- `default`: Resposta de erro padrão.

### 2. Recomendação de Notícias

**`POST /news-recommendation/infer`**  
Retorna recomendações de notícias com base no histórico do usuário.

**Parâmetros Query:**
- `name` BetelgeuseNN
- `id` 2025-02-15-21-17-39

**Corpo da Requisição:**
```json
{
    "user_id": "someUserId",
    "views": [
        {
            "news_id": "390ff660-c693-4f49-be14-b5b88b576856",
            "scroll_percentage": 85.7,
            "time_on_page": 16,
            "viewed_at": "2022-03-08 12:59:24"
        },
        {
            "news_id": "0ecd3141-115e-42e6-8ff0-9fdd2b346c3b",
            "scroll_percentage": 47.3,
            "time_on_page": 21,
            "viewed_at": "2022-03-07 16:59:24"
        },
        {
            "news_id": "455982e9-37ce-46b1-b86b-af48552e5e6a",
            "scroll_percentage": 63.1,
            "time_on_page": 11,
            "viewed_at": "2022-02-28 23:12:45"
        },
        {
            "news_id": "12aba56e-f7f5-4041-8b3b-9ad6649758a6",
            "scroll_percentage": 41.1,
            "time_on_page": 8,
            "viewed_at": "2022-03-08 12:58:24"
        }
    ]
}
```

**Resposta:**
- `200 OK` (JSON)
```json
{
    "model_id": "2025-02-15-21-17-39",
    "model_name": "BetelgeuseNN",
    "output": [
        "ebd223ab-9d97-429f-bf02-1781477f2653",
        "340f9f0b-98b1-4a18-a339-7bf927198911",
        "292d82a1-5e96-4b3b-8ee7-e696f3aa771c",
        "78cd9782-3466-4808-a231-41608c2e4d1b",
        "9c764c3a-f9f8-4fb2-b2c4-6331eaeb3dd6",
        "40908b83-0102-4e6c-9467-58dd76658be0",
        "97897a8d-6c32-47b1-b890-b465a0a24e6c",
        "9fd6edda-5f28-4d58-a726-89da76b2a948",
        "ee583992-5e6d-4e5f-a373-ae9825c79f6a",
        "3ff02906-179b-4d74-a455-07c0663f7d08"
    ]
}
```
- `422`: Erro de validação.
- `default`: Resposta de erro padrão.









