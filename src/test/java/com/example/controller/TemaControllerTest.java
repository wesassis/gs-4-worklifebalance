package com.example.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TemaController.class)
class TemaControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void deveRetornarInformacoesDoTema() throws Exception {
        mockMvc.perform(get("/info"))
                .andExpect(status().isOk())
                .andExpect(content().contentType("application/json"))
                .andExpect(jsonPath("$.tema").value("Aplicativos para conciliar vida pessoal e profissional"))
                .andExpect(jsonPath("$.membro1").value("Wesley Assis RM 552516"))
                .andExpect(jsonPath("$.membro2").value("Guilherme Cavalcanti RM 98928"))
                .andExpect(jsonPath("$.descricao").exists());
    }

    @Test
    void deveCarregarContextoDaAplicacao() throws Exception {
        // Este teste verifica se o controller carrega corretamente
        mockMvc.perform(get("/info"))
                .andExpect(status().isOk());
    }
}