# Documentação do Projeto

## 1. Visão Geral

Este projeto é uma **plataforma acadêmica** que automatiza a consulta e o processamento de currículos de professores. Ele utiliza web scraping para extrair dados do site Escavador, gera resumos e informações adicionais (como área de atuação e títulos dos três últimos projetos) utilizando a API Gemini, e armazena essas informações em um banco de dados PostgreSQL. Além disso, o sistema possui uma interface de usuário (CLI) para consulta e atualização dos dados, bem como um módulo de autenticação para gerenciamento de usuários (alunos).

---

## 2. Tecnologias Utilizadas

- **Python:**  
  Linguagem de programação escolhida por sua versatilidade, legibilidade e vasto ecossistema de bibliotecas.

- **Selenium:**  
  Utilizado para web scraping, permitindo automatizar a navegação e extração de dados do site Escavador.

- **Google Generative AI (Gemini API):**  
  Responsável por processar e resumir os currículos. A API é utilizada para gerar um resumo conciso do currículo, identificar a área de atuação predominante e extrair os títulos dos três últimos projetos do professor.

- **PostgreSQL:**  
  Banco de dados relacional utilizado para armazenar e gerenciar os dados extraídos e processados. Garante integridade referencial e escalabilidade.

- **psycopg2:**  
  Biblioteca Python para interagir com o banco de dados PostgreSQL, utilizando pool de conexões para otimização dos recursos.

- **SQLite:**  
  Uma alternativa utilizada para testes ou operações locais, embora o foco principal seja o PostgreSQL.

- **dotenv:**  
  Gerencia variáveis de ambiente, mantendo informações sensíveis, como a chave da API e credenciais do banco, fora do código-fonte.

---

## 3. Fluxo de Funcionamento do Sistema

### 3.1 Módulo de Scraping e Processamento de Currículos

1. **Inicialização (main2.py):**
   - O sistema carrega as configurações a partir de um arquivo `.env`, onde estão definidas variáveis como `GEMINI_API_KEY` e a lista de professores.
   - O banco de dados é verificado e, se necessário, as tabelas são criadas ou ajustadas para garantir que possuam as colunas necessárias (por exemplo, para armazenar o resumo e o status dos professores).
   - Professores são inseridos no banco se ainda não estiverem cadastrados.

2. **Web Scraping (ScraperFacade & Handlers):**
   - A classe **ScraperFacade** inicializa o WebDriver do Selenium e utiliza uma cadeia de handlers (Chain of Responsibility) para executar as etapas do scraping:
     - **OpenSiteHandler:** Abre o site Escavador.
     - **SearchProfessorHandler:** Realiza a busca pelo professor.
     - **ClickProfileHandler:** Clica no perfil do professor encontrado.
     - **SaveResumeHandler:** Extrai o currículo, salva o arquivo e invoca o módulo de resumo.

3. **Processamento com a API Gemini (gemini_summarizer.py):**
   - O currículo salvo é lido e um prompt é construído para solicitar à API Gemini:
     - Um **resumo** conciso do currículo.
     - A **área de atuação predominante** do professor (ex.: "inteligência artificial", "ciência de dados", "segurança", etc).
     - Os **títulos dos três últimos projetos** desenvolvidos.
   - A resposta é esperada no formato JSON. Delimitadores markdown são removidos, se presentes, para que o parse com `json.loads()` seja realizado corretamente.
   - O JSON resultante é salvo em um arquivo cujo nome é formado a partir do nome do professor (ex.: `response_Victor_André_Pinho_de_Oliveira.json`), evitando conflitos com arquivos de outros professores.

4. **Notificação e Atualização (Observer Pattern):**
   - O **SaveResumeHandler** notifica os observadores (StatusLogger e PostgresSummaryUpdater) com o status do processo e o JSON extraído.
   - O **PostgresSummaryUpdater** atualiza o banco de dados:
     - Atualiza o resumo do currículo do professor.
     - Atualiza a área de atuação na tabela associativa `professor_grande_area`. O texto da área é convertido para o seu ID correspondente na tabela `grande_area` (cria o registro se necessário).
     - Atualiza os projetos do professor na tabela `professor_projeto`. O título do projeto é mapeado para o seu ID na tabela `projeto` (cria o registro se necessário).

### 3.2 Módulo de Gerenciamento e Interface

1. **Banco de Dados e Repositórios:**
   - As classes de repositório (como **ProfessorRepository**, **PerfilRepository**, etc.) gerenciam as operações de CRUD (criação, leitura, atualização e exclusão) no banco de dados PostgreSQL.
   - O **PostgreSQLConnectionSingleton** garante que apenas uma instância de conexão seja utilizada durante a execução do sistema, otimizando o uso de recursos.

2. **Interface de Usuário (CLI):**
   - A interface CLI permite que alunos e administradores consultem professores, alunos e projetos, além de cadastrar e atualizar seus perfis.
   - Operações como sugerir novos professores e atualizar áreas de interesse ou projetos são realizadas por meio do **Facade**, que abstrai a complexidade das interações com os repositórios.

3. **Autenticação:**
   - O sistema possui um módulo de autenticação que utiliza o padrão **Proxy**. A interface **LoginInterface** define o contrato de autenticação, enquanto as classes **LoginReal** e **LoginProxy** implementam essa interface.
   - O **LoginProxy** controla tentativas excessivas de login, bloqueando temporariamente o acesso após múltiplas falhas para aumentar a segurança.

---

## 4. Padrões de Projeto Utilizados

### 4.1 Facade
- **Uso:** Simplifica a interação entre diferentes módulos do sistema (scraping, banco de dados e interface).
- **Motivo:** Permite que o cliente (por exemplo, o módulo principal ou a interface CLI) interaja com uma única interface simplificada, sem precisar conhecer os detalhes internos de cada componente.

### 4.2 Singleton
- **Uso:** Gerenciamento de conexões com o banco de dados (PostgreSQLConnectionSingleton).
- **Motivo:** Garante que apenas uma instância da conexão com o banco seja criada, evitando problemas de concorrência e desperdício de recursos.

### 4.3 Chain of Responsibility
- **Uso:** Implementado nos handlers do módulo de scraping (OpenSiteHandler, SearchProfessorHandler, ClickProfileHandler, SaveResumeHandler).
- **Motivo:** Permite que cada etapa do processo de scraping seja modular e facilmente extensível, delegando a responsabilidade para o próximo handler da cadeia.

### 4.4 Observer
- **Uso:** Notificação de alterações no status do scraping.
- **Motivo:** Facilita a comunicação entre o módulo de scraping e o módulo de atualização do banco de dados, permitindo que múltiplos observadores (como loggers e atualizadores de resumo) sejam notificados automaticamente quando o status do processo mudar.

### 4.5 Proxy
- **Uso:** Implementação da autenticação.
- **Motivo:** Controla e restringe as tentativas de login, aumentando a segurança e prevenindo ataques de força bruta.

---

## 5. Conclusão

Este projeto integra diversas tecnologias e padrões de projeto para criar uma solução robusta e escalável para o processamento e gerenciamento de currículos acadêmicos. A combinação de web scraping, inteligência artificial e um sistema de banco de dados bem estruturado permite a atualização automática dos dados dos professores. Ao mesmo tempo, a interface CLI e o módulo de autenticação garantem a interação segura e intuitiva dos usuários.

A modularidade do sistema, aliada ao uso de padrões como Facade, Singleton, Chain of Responsibility, Observer e Proxy, facilita a manutenção e a futura expansão do projeto.

---


