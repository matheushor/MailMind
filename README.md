MailMind - Classificação Inteligente de Emails
Visão Geral do Projeto
O MailMind é uma solução digital desenvolvida para grandes empresas do setor financeiro que lidam com um alto volume de e-mails diariamente. Nosso objetivo principal é automatizar a leitura, classificação e sugestão de respostas automáticas para esses e-mails, com base no seu teor, liberando a equipe para tarefas mais complexas e estratégicas.

A aplicação utiliza Inteligência Artificial (IA) para categorizar e-mails como "Produtivos" (aqueles que exigem ação imediata, como solicitações de status, problemas ou dúvidas) ou "Improdutivos" (mensagens informativas, agradecimentos genéricos ou irrelevantes). Para cada e-mail, a IA também sugere uma resposta concisa e profissional, otimizando o fluxo de trabalho e melhorando a eficiência operacional.

Funcionalidades
Classificação Inteligente de E-mails: Categoriza e-mails como "Produtivo" ou "Improdutivo" com base no conteúdo.

Sugestão de Respostas Automáticas: Gera respostas personalizadas e profissionais para cada e-mail, adaptadas à sua classificação.

Análise de Confiança: Fornece um nível de confiança para cada classificação da IA, permitindo revisão humana em casos de baixa certeza.

Justificativa da Classificação: A IA explica o raciocínio por trás de cada classificação e sugestão de resposta.

Suporte a Múltiplos Formatos: Aceita conteúdo de e-mails via colagem de texto ou upload de arquivos .txt e .pdf.

Fallback Robusto: Em caso de falha na comunicação com a API de IA, o sistema ainda tenta uma classificação básica por palavras-chave e oferece uma resposta de fallback, garantindo a continuidade do serviço.

Tecnologias Utilizadas
Backend: Python 3.x

Flask: Framework web para o desenvolvimento da API.

Flask-CORS: Para lidar com políticas de segurança de requisições entre diferentes origens.

Google Gemini API (Gemini 1.5 Flash): Para Processamento de Linguagem Natural (NLP), classificação e geração de texto.

PyPDF2: Para extração de texto de arquivos PDF.

requests, json, datetime, uuid, werkzeug.utils.secure_filename: Bibliotecas padrão para operações diversas.

Gunicorn: Servidor WSGI para deploy em produção (ex: Heroku).

Frontend:

HTML5: Estrutura da interface do usuário.

Tailwind CSS: Framework CSS para estilização rápida e responsiva.

JavaScript: Lógica de interação do usuário, envio de dados e atualização da interface.

Font Awesome: Ícones para a interface.

Configuração do Ambiente Local
Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

1. Clonar o Repositório
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO # Navegue até a pasta do projeto

(Substitua SEU_USUARIO e SEU_REPOSITORIO pelos dados reais do seu repositório GitHub.)

2. Criar e Ativar um Ambiente Virtual
É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

3. Instalar Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

pip install -r requirements.txt
# Se o arquivo requirements.txt não existir, gere-o primeiro:
# pip freeze > requirements.txt
# Certifique-se de que Flask, Flask-CORS, requests, PyPDF2 e gunicorn estão listados.

Se você não tiver o requirements.txt e precisar instalá-los individualmente:

pip install Flask Flask-CORS requests PyPDF2 gunicorn

4. Configurar a Chave da API Google Gemini
Você precisará de uma chave da API Google Gemini. Obtenha-a em aistudio.google.com.

Defina a chave como uma variável de ambiente (recomendado para segurança):

No Windows (PowerShell):

$env:GOOGLE_API_KEY="SUA_CHAVE_GEMINI_AQUI"

No Windows (CMD):

set GOOGLE_API_KEY=SUA_CHAVE_GEMINI_AQUI

No macOS/Linux:

export GOOGLE_API_KEY="SUA_CHAVE_GEMINI_AQUI"

(Para torná-la permanente no Windows, adicione-a nas Variáveis de Ambiente do Sistema.)

Alternativamente (apenas para testes rápidos, não recomendado para produção), você pode embutir a chave diretamente no app.py:

GOOGLE_API_KEY = "SUA_CHAVE_GEMINI_AQUI" # Substitua pela sua chave real

(Lembre-se de remover a chave antes de subir para um repositório público!)

5. Executar a Aplicação
Na pasta raiz do projeto, com o ambiente virtual ativado:

python app.py

A aplicação estará acessível em http://127.0.0.1:5000/.

Como Usar
Acesse a Interface: Abra seu navegador e vá para http://127.0.0.1:5000/.

Insira o Conteúdo do E-mail:

Colar Texto: Digite ou cole o conteúdo do e-mail diretamente na área de texto fornecida.

Upload de Arquivo: Clique na área de upload para selecionar um arquivo .txt ou .pdf contendo o e-mail.

Classificar: Clique no botão "Classificar Email".

Visualizar Resultados: A aplicação exibirá a categoria (Produtivo/Improdutivo), o nível de confiança, o raciocínio da IA e uma resposta sugerida.

Implantação (Deploy)
Este projeto pode ser facilmente implantado em plataformas como o Heroku. Certifique-se de ter um Procfile e requirements.txt configurados corretamente, e defina sua GOOGLE_API_KEY como uma variável de ambiente no Heroku.

Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias.

Licença
Este projeto está licenciado sob a Licença MIT.
