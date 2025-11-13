# 🧪 Guia de Testes dos Workflows GitHub Actions

## ✅ Testes Executados

### 1️⃣ **Workflow de Versionamento (Versioning)**
**Teste realizado:** Push na branch `main`
- ✅ **Arquivo modificado:** README.md (título atualizado)
- ✅ **Commit:** "test: atualiza título do README para testar workflow de versionamento"
- ✅ **Push executado:** `git push origin main`

**Resultado esperado:**
- Execução do workflow `Versionamento Automatico`
- Criação de tag automática (v1.0.0, v1.0.1, etc.)
- Visível em: GitHub > Actions > Workflows

### 2️⃣ **Workflow de CI (Continuous Integration)**
**Teste realizado:** Push na branch `feature/test-ci-workflow`
- ✅ **Branch criada:** `feature/test-ci-workflow`
- ✅ **Arquivo criado:** TESTE_CI.md
- ✅ **Commit:** "feat: adiciona arquivo de teste para workflow CI"
- ✅ **Push executado:** `git push origin feature/test-ci-workflow`

**Resultado esperado:**
- Execução do workflow `Continuous Integration (CI)`
- Build da aplicação (mvn clean compile + mvn package)
- Execução de testes unitários (mvn test)
- Build da imagem Docker para verificação
- Visível em: GitHub > Actions > Workflows

### 3️⃣ **Workflow de CD (Continuous Delivery)**
**Teste realizado:** Push na branch `develop` (preparação para PR)
- ✅ **Branch utilizada:** `develop`
- ✅ **Arquivo criado:** TESTE_CD.md
- ✅ **Commit:** "feat: adiciona arquivo de teste para workflow CD"
- ✅ **Push executado:** `git push origin develop`

**Para ativar o workflow CD:**
1. Acesse: https://github.com/wesassis/gs-4-worklifebalance
2. Clique em "Pull requests"
3. Clique em "New pull request"
4. Selecione: `base: develop` ← `compare: qualquer branch com mudanças`
5. Crie o Pull Request

**Resultado esperado:**
- Execução do workflow `Continuous Delivery (CD)`
- Build da aplicação
- Login no Docker Hub (se secrets configuradas)
- Push da imagem para Docker Hub: `wesassis/gs-4-worklifebalance:latest`

## 📋 Como Verificar os Resultados

### 1. **Acessar GitHub Actions**
```
https://github.com/wesassis/gs-4-worklifebalance/actions
```

### 2. **Verificar Workflows Executados**
- **Versionamento:** Deve aparecer execução após push na main
- **CI:** Deve aparecer execução após push na feature/test-ci-workflow
- **CD:** Deve aparecer execução após criar PR para develop

### 3. **Verificar Tags Criadas**
```
https://github.com/wesassis/gs-4-worklifebalance/tags
```

### 4. **Verificar Imagem Docker Hub (se CD executar)**
```
https://hub.docker.com/r/wesassis/gs-4-worklifebalance
```

## ⚠️ Requisitos para CD (Docker Hub)

Para o workflow CD funcionar completamente, configure as secrets:
1. GitHub > Settings > Secrets and variables > Actions
2. Adicione:
   - `DOCKER_USERNAME`: seu usuário Docker Hub
   - `DOCKER_PASSWORD`: sua senha Docker Hub

## 🎯 Status dos Testes

- ✅ **Versioning:** Testado (push main executado)
- ✅ **CI:** Testado (push feature executado)  
- ✅ **CD:** Preparado (branch develop pronta para PR)

**Próximo passo:** Criar Pull Request para develop para ativar workflow CD!