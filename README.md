# 📩 MailMind - Classificação Inteligente de Emails

## 📘 Visão Geral do Projeto

**MailMind** é uma solução digital desenvolvida para grandes empresas do setor financeiro que lidam com um alto volume de e-mails diariamente.  
Seu principal objetivo é **automatizar a leitura, classificação e sugestão de respostas automáticas**, com base no conteúdo dos e-mails.  
Isso permite que as equipes se concentrem em tarefas mais estratégicas e de maior valor.

A aplicação utiliza **Inteligência Artificial (IA)** para categorizar os e-mails como:

- ✅ **Produtivos**: Exigem ação imediata (ex: solicitações de status, dúvidas, problemas).
- ❌ **Improdutivos**: Mensagens informativas, agradecimentos ou irrelevantes.

Além disso, o sistema gera **respostas automáticas concisas e profissionais** para cada e-mail, otimizando o fluxo de trabalho.

---

## ⚙️ Funcionalidades

- 📌 **Classificação Inteligente**: Categorização automática como "Produtivo" ou "Improdutivo".
- ✉️ **Sugestão de Respostas**: Respostas profissionais e personalizadas com base no conteúdo.
- 🧠 **Análise de Confiança**: Indicação do grau de certeza da IA para revisão humana, quando necessário.
- 🔍 **Justificativa da Classificação**: Explicação textual do raciocínio da IA.
- 📂 **Suporte a .txt e .pdf**: Colagem de texto ou upload de arquivos.
- 🚨 **Fallback Robusto**: Sistema de emergência por palavras-chave quando a IA falha.

---

## 🧪 Tecnologias Utilizadas

### 🔧 Backend
- `Python 3.x`
- `Flask` – API web
- `Flask-CORS` – Requisições cross-origin
- `Google Gemini API (Gemini 1.5 Flash)` – NLP e geração de texto
- `PyPDF2` – Extração de texto de PDFs
- `requests`, `json`, `datetime`, `uuid`, `werkzeug` – Utilitários
- `Gunicorn` – Servidor WSGI para deploy

### 💻 Frontend
- `HTML5` – Estrutura da interface
- `Tailwind CSS` – Estilização responsiva
- `JavaScript` – Interatividade
- `Font Awesome` – Ícones

---

## 🛠️ Configuração do Ambiente Local

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/matheushor/MailMind.git
cd SEU_REPOSITORIO
```

### 2️⃣ Criar e Ativar um Ambiente Virtual
```
python -m venv venv
```
###

### Windows:
```
.\venv\Scripts\activate
```
### macOS/Linux:
```
source venv/bin/activate
```
### 3️⃣ Instalar as Dependências
```
pip install -r requirements.txt
```
Se necessário, gere o arquivo:
```
pip freeze > requirements.txt
```
Ou instale manualmente:
```
pip install Flask Flask-CORS requests PyPDF2 gunicorn
```
### 4️⃣ Configurar a Chave da API Google Gemini
Obtenha sua chave em https://aistudio.google.com e defina-a como variável de ambiente:
### Windows (PowerShell):
```
$env:GOOGLE_API_KEY="SUA_CHAVE_GEMINI_AQUI"
```
### Windows (CMD)
```
set GOOGLE_API_KEY=SUA_CHAVE_GEMINI_AQUI
```
### macOS/Linux:
```
export GOOGLE_API_KEY="SUA_CHAVE_GEMINI_AQUI"
```
⚠️ Para testes rápidos, pode-se definir no código app.py, mas **NÃO é seguro para produção:**
```
GOOGLE_API_KEY = "SUA_CHAVE_GEMINI_AQUI"
```
### 5️⃣ Executar a Aplicação
Na raiz do projeto, com o ambiente virtual ativado:
```
python app.py
```

Acesse em: http://127.0.0.1:5000

## 💡 Como Usar

1. Acesse a aplicação no navegador.

2. Insira o conteúdo do e-mail:

- 📋 Colagem de texto

- 📎 Upload de .txt ou .pdf

3. Clique em “Classificar Email”

- Visualize os resultados:

- Classificação

- Confiança da IA

- Justificativa

- Resposta sugerida

 ## 📄 Licença
Este projeto está licenciado sob a MIT License.
