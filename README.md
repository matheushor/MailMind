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

