# Importações necessárias para a aplicação Flask e funcionalidades de IA/processamento
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS # Para lidar com requisições de diferentes origens (CORS)
import os # Para interagir com o sistema operacional (ex: criar diretórios, variáveis de ambiente)
import json # Para trabalhar com dados JSON
import requests # Para fazer requisições HTTP para a API Gemini
from datetime import datetime # Para obter a data e hora atuais
import uuid # Para gerar identificadores únicos (UUIDs)
from werkzeug.utils import secure_filename # Para garantir nomes de arquivo seguros em uploads
import PyPDF2 # Para extrair texto de arquivos PDF
import io # Para manipular streams de dados (necessário para PyPDF2 com uploads)

# Inicialização da aplicação Flask
app = Flask(__name__)
CORS(app) # Habilita Cross-Origin Resource Sharing para permitir que o frontend se comunique com o backend

# --- Configuração da Aplicação ---
UPLOAD_FOLDER = 'uploads' # Define a pasta onde arquivos temporários podem ser armazenados 
ALLOWED_EXTENSIONS = {'txt', 'pdf'} # Define as extensões de arquivo permitidas para upload


# SUBSTITUA "SUA_CHAVE_GEMINI_AQUI" PELA SUA CHAVE REAL DA API GEMINI.
GOOGLE_API_KEY = "AIzaSyCIpNLj5xA1AXWchPeUNoIifIIoy91MGUk" 

# Configurações do Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Define o limite máximo para o tamanho dos arquivos de upload (16 MB)

# Garante que a pasta de uploads exista no sistema de arquivos
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Funções Auxiliares ---

def allowed_file(filename):
    """
    Verifica se a extensão de um dado nome de arquivo é permitida.
    Retorna True se a extensão estiver na lista ALLOWED_EXTENSIONS, False caso contrário.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_stream):
    """
    Extrai texto de um stream de arquivo PDF.
    Recebe um objeto tipo BytesIO ou similar (stream de arquivo binário).
    Retorna o texto extraído como uma string ou None em caso de erro na extração.
    """
    try:
        # PyPDF2.PdfReader espera um objeto de arquivo binário
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            # Concatena o texto de cada página. Usa 'or ""' para evitar None se a página estiver vazia.
            text += page.extract_text() or "" 
        return text
    except Exception as e:
        # Imprime o erro no console do servidor para depuração
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

def classify_email_with_gemini(content):
    """
    Envia o conteúdo do e-mail para a API Google Gemini para classificação e sugestão de resposta.
    Aplica um prompt otimizado para melhor controle da IA, garantindo formato JSON e critérios claros.
    Inclui tratamento de erros robusto para falhas da API e um fallback informativo.

    Args:
        content (str): O texto do e-mail a ser classificado e respondido.

    Returns:
        dict: Um dicionário contendo a classificação (category), confiança (confidence),
              razão (reasoning), resposta sugerida (suggestedResponse), ID único (id),
              preview do conteúdo (content) e timestamp.
    """
    
    # --- PROMPT DE IA OTIMIZADO ---
    
    # Ele define o "papel" da IA, os critérios de classificação com exemplos, e o formato de saída obrigatório.
    prompt = f"""
Você é um assistente de IA especializado na classificação e resposta de e-mails em um ambiente de atendimento ao cliente financeiro. Seu objetivo é analisar a intenção de cada e-mail e gerar uma resposta inicial concisa e profissional.

CLASSIFIQUE este e-mail em uma das duas categorias: "Produtivo" ou "Improdutivo".
SUGIRA uma resposta apropriada, útil e focada no cliente, com no máximo 5 frases.

CRITÉRIOS DE CLASSIFICAÇÃO DETALHADOS:
- **PRODUTIVO**: E-mails que exigem alguma **ação, follow-up, análise específica ou resposta customizada**. Isso inclui:
    - Dúvidas, solicitações de informações detalhadas (extrato, saldo, comprovante).
    - Relato de problemas, erros, inconsistências (transação, fatura, acesso).
    - Pedidos de alteração de cadastro, cancelamento, desbloqueio.
    - Reclamações, sugestões que demandam análise.
    - E-mails com anexos importantes que precisam ser processados.

- **IMPRODUTIVO**: E-mails que **NÃO exigem uma ação imediata ou resposta personalizada** além de um reconhecimento. Isso inclui:
    - Agradecimentos genéricos, felicitações, mensagens de cortesia sem conteúdo adicional.
    - Newsletters, comunicados internos, ou informações gerais que não exigem uma resposta individualizada.
    - E-mails de spam ou irrelevantes.
    - Confirmações automáticas de recebimento de e-mail (se o conteúdo for apenas isso).

---
EXEMPLOS DE COMPORTAMENTO ESPERADO (Few-Shot Learning para guiar a IA):
---
EMAIL DE EXEMPLO 1:
Assunto: Problema no Pix
Corpo: Olá, meu pix não caiu na conta, ja faz 2 horas. Podem verificar por favor?

RESPOSTA JSON ESPERADA:
{{
  "category": "Produtivo",
  "confidence": 98,
  "reasoning": "O email indica um problema específico com uma transação Pix que requer investigação e ação imediata.",
  "suggestedResponse": "Prezado(a) cliente, lamentamos o ocorrido com sua transação Pix. Por favor, forneça o comprovante e os dados da transação (data, hora, valor, ID) para que possamos verificar e auxiliar. Estamos priorizando seu caso."
}}

---
EMAIL DE EXEMPLO 2:
Assunto: Agradecimento
Corpo: Só queria agradecer pelo atendimento que tive ontem, foi excelente! Muito obrigado!

RESPOSTA JSON ESPERADA:
{{
  "category": "Improdutivo",
  "confidence": 92,
  "reasoning": "O email é um agradecimento genérico sem solicitação de ação ou informação adicional.",
  "suggestedResponse": "De nada! Ficamos muito felizes em saber que você teve uma excelente experiência com nosso atendimento. É sempre um prazer ajudar! Se precisar de algo mais, conte conosco."
}}
---

CONTEÚDO DO EMAIL A SER ANALISADO AGORA:
---
{content}
---

FORNEÇA A RESPOSTA **APENAS** NO SEGUINTE FORMATO JSON.
É ABSOLUTAMENTE CRÍTICO que a resposta seja um JSON válido e contenha **todas** as chaves especificadas abaixo, sem qualquer texto adicional antes ou depois do JSON.
{{
  "category": "Produtivo" ou "Improdutivo",
  "confidence": <número inteiro de 0 a 100 indicando a certeza da classificação>,
  "reasoning": "<explicação concisa de por que o e-mail foi classificado dessa forma e a lógica da resposta sugerida>",
  "suggestedResponse": "<resposta profissional, personalizada e no máximo 5 frases para este e-mail específico. Se for improdutivo, uma resposta de 'ciente' ou 'obrigado' é suficiente. Se produtivo, aborde a solicitação e indique próximos passos.>"
}}"""

    try:
        # URL da API Gemini para o modelo 1.5 Flash
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        # Payload da requisição HTTP para a API Gemini
        payload = {
            "contents": [{"parts": [{"text": prompt}]}], # O conteúdo do prompt é enviado como parte da requisição
            "generationConfig": {
                # Temperatura mais baixa (0.3) para maior consistência na classificação e no formato JSON.
                # Uma temperatura mais alta (ex: 0.7-0.9) seria para respostas mais criativas/variadas.
                "temperature": 0.3, 
                "maxOutputTokens": 500 # Limite máximo de tokens para a resposta do modelo
            }
        }
        
        # Faz a requisição POST para a API Gemini com o payload JSON
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        
        # Verifica se a requisição foi bem-sucedida (código de status HTTP 200)
        if response.status_code == 200:
            data = response.json() # Decodifica a resposta JSON da API
            
            # --- VALIDAÇÃO APRIMORADA DA RESPOSTA DA API ---
            # Verifica se a resposta contém o campo 'candidates' e se não está vazio
            if 'candidates' not in data or not data['candidates']:
                raise Exception("Resposta da API Gemini inválida: 'candidates' ausente ou vazio.")
            
            # Extrai o texto da resposta do modelo, que deve ser o JSON gerado
            result_text = data['candidates'][0]['content']['parts'][0]['text']
            
            # Remove qualquer formatação de bloco de código (ex: ```json) que o Gemini possa adicionar
            cleaned_result = result_text.replace('```json', '').replace('```', '').strip()
            
            try:
                # Tenta decodificar a string JSON limpa em um objeto Python
                classification = json.loads(cleaned_result)
            except json.JSONDecodeError as jde:
                # Captura erros se o texto não for um JSON válido
                print(f"Erro ao decodificar JSON da API: {jde}")
                print(f"Texto bruto recebido (limpo): {cleaned_result}")
                # Lança uma exceção mais clara para depuração
                raise Exception(f"Formato JSON inválido da API Gemini. Erro: {jde}. Resposta parcial: {cleaned_result[:200]}...")

            # Valida para garantir que todas as chaves esperadas existam no objeto JSON
            required_keys = ['category', 'confidence', 'reasoning', 'suggestedResponse']
            if not all(k in classification for k in required_keys):
                missing_keys = [k for k in required_keys if k not in classification]
                raise Exception(f"Resposta JSON da API Gemini incompleta. Faltam chaves: {', '.join(missing_keys)}.")
            
            # Retorna o resultado formatado como um dicionário, garantindo tipos e valores padrão
            return {
                'id': str(uuid.uuid4()), # ID único para esta entrada de e-mail
                'content': content[:500] + ('...' if len(content) > 500 else ''), # Preview do conteúdo do e-mail (limitado a 500 chars)
                'category': classification.get('category', 'Desconhecido'), # Categoria do e-mail, com fallback 'Desconhecido'
                'confidence': int(classification.get('confidence', 0)), # Nível de confiança da classificação (convertido para int)
                'reasoning': classification.get('reasoning', 'Nenhuma razão fornecida.'), # Razão da classificação
                'suggestedResponse': classification.get('suggestedResponse', 'Nenhuma resposta sugerida.'), # Resposta automática sugerida
                'timestamp': datetime.now().isoformat() # Data e hora da classificação
            }
        else:
            # Em caso de erro HTTP da API (ex: 429 Quota Exceeded, 400 Bad Request),
            # imprime os detalhes do erro e lança uma exceção.
            error_details = response.json() if response.content else {"message": "Nenhum detalhe de erro na resposta."}
            print(f"Erro da API Gemini - Status {response.status_code}: {error_details}")
            raise Exception(f"Erro na comunicação com a API Gemini: Status {response.status_code}. Detalhes: {error_details.get('error', {}).get('message', 'Erro desconhecido')}")
            
    except requests.exceptions.RequestException as req_err:
        # Captura erros relacionados à rede ou à requisição HTTP (ex: sem internet, URL errada)
        print(f"Erro de conexão ou HTTP com a API Gemini: {req_err}")
        api_error_message = f"Erro de rede/conexão com a API: {req_err}"
        # A API pode estar inacessível, o fluxo continuará para o fallback
        
    except Exception as e:
        # Captura outros erros inesperados no processamento da resposta da API (ex: JSON inválido após limpeza)
        print(f"Erro inesperado no processamento da resposta da API: {e}")
        api_error_message = f"Erro de processamento da IA: {e}"
        # Qualquer outro erro, o fluxo continuará para o fallback

    # --- FALLBACK SIMPLES E MAIS DESCRITIVO ---
    # Este é um mecanismo de segurança para que a aplicação não quebre completamente
    # em caso de falha da API Gemini. Tenta classificar por palavras-chave e fornece uma resposta genérica.
    content_lower = content.lower() # Converte o conteúdo para minúsculas para comparação de palavras-chave
    productive_keywords = [
        'dúvida', 'problema', 'ajuda', 'solicita', 'urgente', 'pendente', 'anexo', 
        'cobranca', 'boleto', 'status', 'requer', 'informar sobre', 'cadastro', 
        'reclamacao', 'falha', 'erro', 'acesso', 'senha', 'transação', 'depósito'
    ]
    is_productive = any(word in content_lower for word in productive_keywords)
    
    return {
        'id': str(uuid.uuid4()), # Gera um ID único mesmo no fallback
        'content': content[:500] + ('...' if len(content) > 500 else ''), # Preview do conteúdo
        'category': 'Produtivo' if is_productive else 'Improdutivo', # Classificação baseada em palavras-chave
        'confidence': 30, # Confiança baixa para indicar que é um fallback automático
        'reasoning': f'Classificação automática baseada em palavras-chave (API inacessível ou erro: {api_error_message if "api_error_message" in locals() else "Erro desconhecido no backend"}).',
        'suggestedResponse': 'Obrigado pelo contato. Recebemos sua mensagem. Devido a um problema técnico temporário, nossa IA não pôde processá-la. Retornaremos o mais breve possível com uma resposta personalizada. Agradecemos a compreensão.',
        'timestamp': datetime.now().isoformat()
    }

# --- Rotas Flask ---

@app.route('/')
def index():
    """
    Rota principal que renderiza o template HTML da interface do usuário.
    """
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_email_route(): # Nome da função da rota, para evitar conflito com a função helper 'classify_email_with_gemini'
    """
    Rota para receber o e-mail (via upload de arquivo ou texto direto do formulário),
    enviar para classificação via API Gemini e retornar o resultado JSON para o frontend.
    """
    try:
        content = "" # Variável para armazenar o conteúdo do e-mail
        filename = None # Variável para armazenar o nome do arquivo, se houver

        # --- Processamento de Upload de Arquivo ---
        # Verifica se o campo 'file' (nome do input no index.html) está presente na requisição de arquivos
        if 'file' in request.files: 
            file = request.files['file'] # Obtém o objeto do arquivo enviado
            # Verifica se um arquivo foi realmente selecionado e se tem um nome de arquivo
            if file and file.filename: 
                # Verifica se a extensão do arquivo é permitida
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename) # Limpa o nome do arquivo para segurança
                    
                    if filename.lower().endswith('.pdf'):
                        # Se for PDF, extrai o texto usando a função auxiliar
                        content = extract_text_from_pdf(file.stream)
                        if not content:
                            # Retorna erro se o PDF estiver vazio ou a extração falhar
                            return jsonify({'error': 'Erro ao extrair texto do PDF ou PDF vazio.'}), 400
                    else: # Assume .txt ou outro formato de texto simples
                        # Lê o conteúdo do arquivo e decodifica para UTF-8
                        content = file.read().decode('utf-8')
                else:
                    # Retorna erro se a extensão do arquivo não for permitida
                    return jsonify({'error': 'Tipo de arquivo não permitido.'}), 400
            # Se 'file' estiver em request.files, mas file.filename for vazio, significa que
            # o input de arquivo foi enviado, mas nenhum arquivo foi realmente selecionado.
            # Essa condição será capturada pelo `if not content.strip():` mais abaixo.

        # --- Processamento de Texto Direto ---
        # Se nenhum conteúdo foi extraído de um arquivo (ou nenhum arquivo foi enviado/válido),
        # verifica se há texto no campo 'content' do formulário (nome do textarea no index.html)
        if not content and 'content' in request.form: 
            content = request.form['content'] # Obtém o texto do campo de formulário
        
        # --- Processamento de Requisição JSON Direta (para testes de API, por exemplo) ---
        # Se ainda não há conteúdo e a requisição é do tipo JSON
        elif not content and request.is_json:
            data = request.get_json() # Obtém os dados JSON do corpo da requisição
            content = data.get('content', '') # Tenta obter o 'content' do JSON, com default vazio
        
        # --- Validação Final de Conteúdo ---
        # Se após todas as verificações, 'content' ainda estiver vazio ou for apenas espaços em branco
        if not content.strip():
            # Retorna um erro indicando que nenhuma entrada de e-mail foi fornecida
            return jsonify({'error': 'Nenhum conteúdo de email fornecido para classificação (nem arquivo, nem texto).'}), 400
        
        # Chama a função principal de classificação com a IA
        result = classify_email_with_gemini(content)
        # Adiciona o nome do arquivo ao resultado, se houver, ou 'Não aplicável'
        result['fileName'] = filename if filename else 'Não aplicável' 
        
        # Retorna o resultado JSON para o frontend
        return jsonify(result)
        
    except Exception as e:
        # Captura qualquer exceção não tratada na rota e imprime no console do servidor
        print(f"Erro fatal na rota /classify: {e}")
        # Retorna uma mensagem de erro genérica para o frontend
        return jsonify({'error': f'Erro interno no processamento: {str(e)}'}), 500

# --- Execução da Aplicação ---
if __name__ == '__main__':
    # Inicia o servidor Flask.
    # debug=True: Ativa o modo de depuração (recarrega o servidor ao salvar, mostra erros detalhados).
    # host='0.0.0.0': Permite que o servidor seja acessível de outras máquinas na rede (útil para testes em diferentes dispositivos).
    # port=5000: Define a porta em que o servidor irá rodar.
    app.run(debug=True, host='0.0.0.0', port=5000)

