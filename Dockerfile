FROM eclipse-temurin:17-jdk-alpine 
  
ARG JAR_FILE=target/gs-4-worklifebalance-*.jar 
  
WORKDIR /app 
  
COPY ${JAR_FILE} app.jar 
  
EXPOSE 8081 
  
ENTRYPOINT ["java", "-jar", "app.jar"] 
