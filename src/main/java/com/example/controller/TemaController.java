package com.example.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.Map;
import java.util.LinkedHashMap;

@RestController
@Tag(name = "Tema Controller", description = "API para informações sobre o tema da Global Solution")
public class TemaController {

    @GetMapping("/info")
    @Operation(
        summary = "Retorna informações sobre o tema da Global Solution",
        description = "Endpoint que retorna informações sobre aplicativos para conciliar vida pessoal e profissional"
    )
    @ApiResponse(responseCode = "200", description = "Informações retornadas com sucesso")
    public Map<String, String> getInfo() {
        Map<String, String> info = new LinkedHashMap<>();
        info.put("tema", "Aplicativos para conciliar vida pessoal e profissional");
        info.put("membro1", "Wesley Assis RM 552516");
        info.put("membro2", "Guilherme Cavalcanti RM 98928");
        info.put("descricao", "API para a Global Solution sobre o tema de aplicativos para conciliar vida pessoal e profissional.");
        
        return info;
    }

    @GetMapping("/status")
    @Operation(
        summary = "Retorna status da aplicação",
        description = "Endpoint para verificar se a aplicação está funcionando corretamente"
    )
    @ApiResponse(responseCode = "200", description = "Status retornado com sucesso")
    public Map<String, String> getStatus() {
        Map<String, String> status = new LinkedHashMap<>();
        status.put("status", "UP");
        status.put("version", "1.0.0");
        status.put("timestamp", java.time.LocalDateTime.now().toString());
        status.put("message", "Pipeline CD funcionando corretamente!");
        
        return status;
    }
}