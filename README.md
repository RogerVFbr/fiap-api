# FIAP Tech Challenge: Stock Price Prediction *(Fase 4)*

## Enunciado
Criar um modelo preditivo de redes neurais Long Short Term Memory (LSTM) para predizer o valor de fechamento da bolsa 
de valores de uma empresa à sua escolha e realizar toda a pipeline de desenvolvimento, desde a criação do modelo 
preditivo até o deploy do modelo em uma API que permita a previsão de preços de ações.

## Requisitos

### Coleta e pré-processamento de dados
* **Coleta de Dados.** Dataset pré tratado e persistido no repositório de modelo para simplificação da implementação.
* **Construção do Modelo.** Feita no repositório de modelo.
* **Avaliação.** Utiliza-se de uma função de *loss* baseada em RSME.

### Salvamento e Exportação do Modelo
* **Salvar o Modelo.** O modelo é salvo em disco e posteriormente publicado em
um Bucket S3 via esteira.

### Deploy do Modelo
* **Criação da API.** Foi criada uma API Serverless que carrega o modelo em tempo de execução.

### Escalabilidade e Monitoramento
* **Monitoramento.** Utiliza-se AWS Cloudwatch para publicação de lgos e telemetria.

## Entregáveis

* **Código-fonte e documentação.** O código fonte da solução é dividido em dois repositórios, um para a criação do modelo
e outro para a API. Este repositório contém o diagrama de solução, README.md explicativo e uma collection (Insomnia)
para testes e validação da API.
* **Scripts ou contêineres Docker para deploy da API.** O processo de CI/CD utiliza Github para versionamento, Github Actions
para automatização da implantação e Terraform para subida de infra e execução de scripts. Cada um dos dois repositórios
da solução possui suas definições individuais.
* **Link para a API em produção, caso tenha sido publicada em um ambiente de nuvem.** Em arquivo anexo na entrega do trabalho.
* **Vídeo mostrando e explicando todo o funcionamento da APl.** Em arquivos anexos na entrega do trabalho.


