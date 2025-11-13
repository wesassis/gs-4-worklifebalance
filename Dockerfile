# Multi-stage Docker build
# Stage 1: Build da aplicação
FROM eclipse-temurin:17-jdk AS builder

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do Maven
COPY pom.xml .
COPY src ./src

# Instala Maven
RUN apt-get update && apt-get install -y maven && apt-get clean

# Executa o build da aplicação
RUN mvn clean package -DskipTests

# Stage 2: Runtime da aplicação
FROM eclipse-temurin:17-jre

# Define diretório de trabalho
WORKDIR /app

# Copia o JAR da aplicação do stage anterior
COPY --from=builder /app/target/gs-4-worklifebalance-*.jar app.jar

# Expõe a porta 8081
EXPOSE 8081

# Define variáveis de ambiente
ENV JAVA_OPTS="-Xmx512m -Xms256m"

# Comando para executar a aplicação
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]