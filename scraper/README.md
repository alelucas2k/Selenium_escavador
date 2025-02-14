# 🔍 Plataforma de Consulta de Currículos Acadêmicos

## 📌 **Sobre o Projeto**
Este projeto automatiza a busca e o resumo de currículos acadêmicos de professores, extraindo informações do site **Escavador** e armazenando-as em um banco de dados. Ele permite consultar pesquisas e projetos dos professores de forma simplificada, utilizando web scraping e processamento de linguagem natural (via API Gemini).

## 🚀 **Fluxo de Execução**
1. **Iniciação do Sistema**
   - O script principal (`main2.py`) carrega configurações do arquivo `.env`.
   - Verifica e cria a tabela no banco de dados, caso não exista.
   - Obtém uma lista de professores pendentes para processamento.

2. **Web Scraping - Extração do Currículo**
   - Utiliza **Selenium** para acessar o site do Escavador.
   - Passa por uma cadeia de manipuladores (**Chain of Responsibility**) para realizar:
     - **Abertura do site**
     - **Busca pelo professor**
     - **Clique no perfil correto**
     - **Extração e salva o currículo**

3. **Geração de Resumo com API Gemini**
   - O texto do currículo é enviado para a API Gemini.
   - Um resumo conciso é gerado, destacando as pesquisas do professor.
   - O resumo é salvo e atualizado no banco de dados.

4. **Armazenamento no Banco de Dados**
   - Utiliza **PostgreSQL** e **SQLite** para armazenar dados.
   - Atualiza o status dos professores processados.

## 🏗 **Padrões de Projeto Utilizados**

### 1️⃣ **Facade**
   - **Arquivos**: `scraper_facade.py`, `main2.py`
   - **Motivo**: Simplifica a interação com componentes complexos (scraping e banco de dados), oferecendo uma interface única.

### 2️⃣ **Singleton**
   - **Arquivos**: `database.py`, `repository.py`
   - **Motivo**: Garante que haja apenas uma instância da conexão com o banco, evitando desperdício de recursos.

### 3️⃣ **Factory Method + Chain of Responsibility**
   - **Arquivos**: `handlers_factory.py`, `driver_handlers.py`
   - **Motivo**: Modulariza cada etapa do scraping, permitindo adicionar ou modificar handlers sem impactar o fluxo principal.

### 4️⃣ **Observer**
   - **Arquivos**: `observer.py`
   - **Motivo**: Permite que diferentes partes do sistema (logs, banco) sejam notificadas automaticamente sobre mudanças de status.

### 5️⃣ **Helper/Utilitário**
   - **Arquivos**: `gemini_summarizer.py`
   - **Motivo**: Centraliza a comunicação com a API Gemini, garantindo separação de responsabilidades.

## 📂 **Estrutura do Projeto**
```
📁 projeto
│-- 📄 main2.py                # Ponto de entrada da aplicação
│-- 📄 scraper_facade.py       # Interface simplificada para scraping
│-- 📄 database.py             # Gerenciamento da conexão com o banco
│-- 📄 repository.py           # Manipulação dos dados dos professores
│-- 📄 handlers_factory.py     # Cria a cadeia de handlers do scraping
│-- 📄 driver_handlers.py      # Etapas do scraping (busca, clique, extração)
│-- 📄 observer.py             # Notificações sobre o status do scraping
│-- 📄 gemini_summarizer.py    # Resumo do currículo usando Gemini
│-- 📄 .env                    # Variáveis de ambiente (chaves de API, configuração do BD)
```

## 🛠 **Tecnologias Utilizadas**
- **Python**
- **Selenium** (Web Scraping)
- **PostgreSQL + SQLite** (Banco de Dados)
- **Google Gemini API** (Geração de resumos)
- **Padrões de Projeto** (Facade, Observer, Singleton, Factory, Chain of Responsibility)

## 📌 **Como Executar o Projeto**
### 1️⃣ Instalar Dependências:


### 2️⃣ Configurar `.env`:
Crie um arquivo `.env` com:
```
GEMINI_API_KEY= sua-chave-aqui
PROFESSORES_LIST=Nome1, Nome2, Nome3
```
### 3️⃣ Executar o Script:
```sh
python main2.py
```


---
Este projeto facilita a consulta a currículos acadêmicos, proporcionando um acesso mais rápido e eficiente a informações sobre pesquisas e projetos. 🚀

