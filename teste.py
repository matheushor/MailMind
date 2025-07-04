import requests
import json

GOOGLE_API_KEY = "AIzaSyAnU_rYsJ925aMtwu3Z8CXEXWTjV20qx18"

def test_gemini_api(content):
    prompt = f"""
Classifique este email como "Produtivo" ou "Improdutivo" e sugira uma resposta apropriada.

CRITÉRIOS:
- PRODUTIVO: Requer ação (dúvidas, solicitações, problemas)
- IMPRODUTIVO: Não requer ação imediata (agradecimentos, informações)

CONTEÚDO: {content}

Responda SOMENTE com JSON válido, sem texto adicional. O JSON deve conter:
- "category": string ("Produtivo" ou "Improdutivo")
- "confidence": número inteiro de 0 a 100
- "reasoning": string (explicação breve)
- "suggestedResponse": string (resposta apropriada para o email)

Exemplo de resposta JSON:
{{
  "category": "Produtivo",
  "confidence": 85,
  "reasoning": "O email contém uma solicitação urgente.",
  "suggestedResponse": "Obrigado pelo contato, estamos verificando seu problema."
}}
"""

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 500
        }
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    print("Status code:", response.status_code)
    print("Resposta bruta da API:")
    print(response.text)

    if response.status_code == 200:
        try:
            data = response.json()
            result_text = data['candidates'][0]['content']['parts'][0]['text']
            print("\nTexto retornado pelo modelo:")
            print(result_text)

            # Limpar possíveis backticks e espaços
            cleaned_result = result_text.replace('```json', '').replace('```', '').strip()

            classification = json.loads(cleaned_result)
            print("\nJSON parseado:")
            print(json.dumps(classification, indent=2))

            return classification
        except Exception as e:
            print("Erro ao parsear JSON:", e)
    else:
        print("Erro na requisição:", response.status_code, response.text)


if __name__ == "__main__":
    exemplo_email = """Olá, estou com um problema no sistema que precisa ser resolvido com urgência. Pode ajudar?"""
    test_gemini_api(exemplo_email)
