"""
Padrão utilizado: Helper/Utilitário.
Explicação:
Este módulo centraliza a lógica para resumir currículos utilizando a API Gemini,
isolando a responsabilidade de comunicação com o serviço externo.
Dessa forma, facilita a reutilização e manutenção da função de resumo no sistema.
"""


import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Obtém a chave da API do Gemini a partir da variável de ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Chave da API não encontrada. Verifique o arquivo .env.")

# Configura a biblioteca com sua API key
genai.configure(api_key=GEMINI_API_KEY)


def resumir_curriculo_gemini(nome_arquivo):
    """
    Lê o arquivo de currículo e utiliza a API Gemini para gerar um resumo.
    O prompt é configurado para que o modelo resuma o texto de forma concisa em um parágrafo.

    Parâmetros:
        nome_arquivo (str): caminho do arquivo com o currículo.

    Retorna:
        resumo (str): o texto resumido ou None em caso de erro.
    """
    try:
        # Lê o conteúdo do currículo
        with open(nome_arquivo, "r", encoding="utf-8") as file:
            conteudo = file.read()

        # Cria o prompt para resumir
        prompt = f"Resuma o seguinte currículo de forma concisa dando foco ao tipo de projeto de pesquisa que o professor costuma trabalhar:\n\n{conteudo}"

        # Instancia o modelo Gemini (a versão utilizada pode ser ajustada conforme necessidade)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        # Chama o metodo generate_text na instancia do modelo
        response = model.generate_content(prompt)

        # Extrai o resumo da resposta
        resumo = response.text.strip()

        # Salva o resumo em um novo arquivo (substituindo "curriculo_" por "resumo_")
        nome_resumo = nome_arquivo.replace("curriculo_", "resumo_")
        with open(nome_resumo, "w", encoding="utf-8") as file:
            file.write(resumo)
        print(f"Resumo salvo em '{nome_resumo}'")

        return resumo
    except Exception as e:
        print(f"Erro ao resumir usando Gemini: {e}")
        return None
