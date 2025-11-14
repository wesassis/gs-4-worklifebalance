# 🌟 Global Solution - Work-Life Balance API 

## 👥 Integrantes do Grupo

- **Wesley Assis** - RM 552516
- **Guilherme Cavalcanti** - RM 98928

## 📋 Descrição do Tema

**Tema 4:** Aplicativos para conciliar vida pessoal e profissional

Esta API foi desenvolvida para a Global Solution com foco em soluções tecnológicas que ajudam pessoas a equilibrarem suas vidas pessoais e profissionais através de aplicações digitais inovadoras.

## 🎯 Finalidade da API

A API fornece informações estruturadas sobre o tema da Global Solution através de um endpoint REST simples, servindo como base para futuras funcionalidades relacionadas a aplicativos de work-life balance e demonstrando boas práticas de desenvolvimento moderno.

## 🛠️ Tecnologias Utilizadas

- **Java 17+**
- **Spring Boot 3.2.0**
- **Maven** (Gerenciamento de dependências)
- **Swagger/OpenAPI** (Documentação da API)
- **Docker** (Containerização)
- **GitHub Actions** (CI/CD)

## 🚀 Como Executar o Projeto

### 📋 Pré-requisitos

- Java 17 ou superior
- Maven 3.6 ou superior
- Docker (opcional, para execução via container)

### 🏃‍♂️ Execução Local

#### Opção 1: Executando o JAR

```bash
# Clone o repositório
git clone https://github.com/wesassis/gs-4-worklifebalance.git
cd gs-4-worklifebalance

# Compile e empacote a aplicação
mvn clean package

# Execute o JAR gerado
java -jar target/gs-4-worklifebalance-1.0.0.jar
```

#### Opção 2: Executando com Maven

```bash
# Clone o repositório
git clone https://github.com/wesassis/gs-4-worklifebalance.git
cd gs-4-worklifebalance

# Execute diretamente com Maven
mvn spring-boot:run
```

#### Opção 3: Executando com Docker

```bash
# Clone o repositório
git clone https://github.com/wesassis/gs-4-worklifebalance.git
cd gs-4-worklifebalance

# Build da imagem Docker
docker build -t gs-4-worklifebalance .

# Execute o container
docker run -p 8081:8081 gs-4-worklifebalance
```

### 🌐 Acessando a Aplicação

Após executar a aplicação, ela estará disponível em: **http://localhost:8081**

#### 📍 Endpoints Disponíveis

- **GET /info** - Retorna informações sobre o tema da Global Solution
- **GET /swagger-ui.html** - Documentação interativa da API (Swagger UI)
- **GET /api-docs** - Especificação OpenAPI em formato JSON
- **GET /actuator/health** - Health check da aplicação

#### 📄 Exemplo de Resposta do Endpoint /info

```json
{
  "tema": "Aplicativos para conciliar vida pessoal e profissional",
  "membro1": "Wesley Assis RM 552516",
  "membro2": "Guilherme Cavalcanti RM 98928",
  "descricao": "API para a Global Solution sobre o tema de aplicativos para conciliar vida pessoal e profissional."
}
```

## 🐳 Docker Hub

A imagem Docker da aplicação está disponível no Docker Hub:

**🔗 URL da Imagem:** `https://hub.docker.com/r/wesassis/gs-4-worklifebalance`

**🏷️ Tag da Imagem:** `wesassis/gs-4-worklifebalance:latest`

### Executando a imagem do Docker Hub

```bash
# Pull e execução da imagem
docker run -p 8081:8081 wesassis/gs-4-worklifebalance:latest
```

## ⚙️ CI/CD Pipeline

O projeto implementa um pipeline completo de **CI/CD** usando **GitHub Actions** com três workflows principais:

### 🏷️ 1. Versionamento Automático (`versioning.yml`)

- **Trigger:** Push na branch `main`
- **Função:** Gera tags automáticas (v1.0.0, v1.0.1, etc.)
- **Ferramenta:** GitHub Tag Action

### 🔨 2. Continuous Integration (`ci.yml`)

- **Trigger:** Push nas branches `feature/**`, `release`, `hotfix`
- **Funções:**
  - Build da aplicação com Maven
  - Execução de testes unitários
  - Verificação do build Docker
  - Upload de artefatos de teste

### 🚀 3. Continuous Delivery (`cd.yml`)

- **Trigger:** Pull Request para branch `develop`
- **Funções:**
  - Build da aplicação
  - Login no Docker Hub
  - Build e push da imagem Docker multi-arquitetura
  - Deploy automático no Docker Hub

### 🔐 Secrets Necessárias

Para o funcionamento completo do pipeline, configure as seguintes secrets no GitHub:

- `DOCKER_USERNAME` - Usuário do Docker Hub
- `DOCKER_PASSWORD` - Senha do Docker Hub

## 📁 Estrutura do Projeto

```
gs-4-worklifebalance/
├── .github/
│   └── workflows/
│       ├── versioning.yml     # Versionamento automático
│       ├── ci.yml             # Continuous Integration
│       └── cd.yml             # Continuous Delivery
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── WorkLifeBalanceApplication.java
│   │   │       ├── config/
│   │   │       │   └── OpenApiConfig.java
│   │   │       └── controller/
│   │   │           └── TemaController.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/example/
│               └── controller/
│                   └── TemaControllerTest.java
├── Dockerfile
├── .dockerignore
├── pom.xml
└── README.md
```

## 🧪 Testes

Execute os testes unitários:

```bash
mvn test
```

Os testes verificam:
- ✅ Resposta correta do endpoint `/info`
- ✅ Carregamento correto do contexto da aplicação
- ✅ Estrutura JSON retornada

