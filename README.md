# Scraper de Currículos com Resumo via Gemini

Este projeto tem como objetivo automatizar a busca por perfis de professores em um website, extrair seus currículos, gerar um resumo utilizando a API Gemini da Google e armazenar os resultados em um banco de dados SQLite.

## Overview

O sistema realiza as seguintes etapas:
- **Busca e Navegação:** Utiliza o Selenium para acessar o site e realizar buscas pelos nomes dos professores.
- **Extração de Dados:** Captura o conteúdo bruto dos currículos diretamente da página.
- **Geração de Resumo:** Envia o texto do currículo para a API Gemini, que retorna um resumo conciso focado no tipo de projeto de pesquisa do professor.
- **Armazenamento:** Atualiza o status do processamento e salva o resumo gerado diretamente no banco de dados SQLite.
- **Notificação:** Utiliza o padrão Observer para notificar diferentes componentes (como log e atualização no banco) sobre o status do processamento.

## Funcionalidades

- **Automação de Navegação:** Abre o site e realiza buscas por professores.
- **Scraping Dinâmico:** Extrai currículos diretamente da página sem salvá-los em arquivos de texto.
- **Geração de Resumo Automatizada:** Processa o currículo bruto com a API Gemini para gerar um resumo.
- **Armazenamento Centralizado:** Registra as informações e o status dos professores em um banco de dados SQLite.
- **Arquitetura Modular:** Utiliza diversos padrões de projeto para manter o código organizado e de fácil manutenção.

## Tecnologias Utilizadas

- **Python:** Linguagem principal do projeto.
- **Selenium:** Para automação e scraping de dados via navegador.
- **ChromeDriverManager:** Gerenciamento automático do driver do Chrome.
- **SQLite:** Banco de dados relacional leve para armazenamento dos dados.
- **dotenv:** Gerenciamento de variáveis de ambiente (por exemplo, chaves de API e lista de professores).
- **Google Generative AI (Gemini):** Serviço de IA utilizado para resumir os currículos.
- **Padrões de Projeto:**  
  - **Factory Method e Chain of Responsibility:** Organiza a criação e o fluxo de execução dos handlers que compõem as etapas do scraping.
  - **Observer:** Notifica componentes responsáveis por log e atualização do banco de dados quanto a mudanças de status.
  - **Singleton:** Garante uma única instância para o acesso ao banco de dados.
  - **Facade:** Simplifica a interação com os componentes internos (como o Selenium e a cadeia de handlers) expondo uma interface única e de fácil utilização.
