"""
Padrão utilizado: Helper/Utilitário.
Explicação:
Este módulo centraliza a lógica para resumir currículos utilizando a API Gemini,
isolando a responsabilidade de comunicação com o serviço externo.
Dessa forma, facilita a reutilização e manutenção da função de resumo no sistema.
"""

import os
import json
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

def limpar_resposta_markdown(text):
    """
    Remove delimitadores de markdown (ex: ```json e ```) da resposta, se presentes.
    """
    texto = text.strip()
    if texto.startswith("```"):
        lines = texto.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        texto = "\n".join(lines).strip()
    return texto

def resumir_e_extrair_info(nome_arquivo, professor=None):
    """
    Lê o arquivo de currículo e utiliza a API Gemini para gerar um resumo e extrair
    informações adicionais (área de atuação e títulos dos 3 últimos projetos), retornando um JSON.
    O arquivo JSON é salvo com o nome 'response_<professor>.json' se o nome do professor for fornecido,
    caso contrário, utiliza 'response_json.json'.
    """
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as file:
            conteudo = file.read()

        prompt = f"""
Resuma o seguinte currículo e extraia as seguintes informações:
1. \"resumo\": Um parágrafo conciso com os principais pontos do currículo.
2. \"area\": A área de atuação predominante do professor (ex: \"inteligência artificial\", \"ciência de dados\", \"segurança\", etc).
3. \"projetos\": Uma lista com os títulos dos três últimos projetos desenvolvidos.
Retorne a resposta no formato JSON.

{conteudo}
"""
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)

        print("Resposta da API:", response.text)
        resposta_limpa = limpar_resposta_markdown(response.text)
        if not resposta_limpa.strip():
            print("Erro: Resposta vazia da API Gemini.")
            return None

        try:
            resultado = json.loads(resposta_limpa)
        except json.JSONDecodeError as decode_error:
            print(f"Erro ao decodificar JSON: {decode_error}. Conteúdo recebido: {resposta_limpa}")
            return None

        # Define o nome do arquivo JSON usando o nome do professor, se fornecido
        if professor:
            professor_filename = professor.replace(" ", "_")
            json_filename = f"response_{professor_filename}.json"
        else:
            json_filename = "response_json.json"

        with open(json_filename, "w", encoding="utf-8") as file:
            json.dump(resultado, file, ensure_ascii=False, indent=4)
        print(f"Resposta JSON salva como '{json_filename}'")

        return resultado  # Espera retornar um dicionário com chaves: "resumo", "area" e "projetos"
    except Exception as e:
        print(f"Erro ao resumir usando Gemini: {e}")
        return None
