# Teste do Workflow CD

Este arquivo foi criado para testar o workflow de Continuous Delivery.

## Funcionalidades Testadas:
- Build da aplicação
- Login no Docker Hub
- Push da imagem para Docker Hub

O workflow CD deve ser disparado por:
- Pull Request para a branch develop

## Imagem Docker:
- Nome: wesassis/gs-4-worklifebalance:latest
- Tag SHA: wesassis/gs-4-worklifebalance:{github.sha}