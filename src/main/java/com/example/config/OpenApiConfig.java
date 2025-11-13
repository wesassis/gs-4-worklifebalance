package com.example.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Global Solution - Work-Life Balance API")
                        .version("1.0.0")
                        .description("API para a Global Solution sobre aplicativos para conciliar vida pessoal e profissional")
                        .contact(new Contact()
                                .name("Wesley Assis & Guilherme Cavalcanti")
                                .email("contato@globalsolution.com")));
    }
}