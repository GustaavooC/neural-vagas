from telethon import TelegramClient, events
import requests
import re
from datetime import datetime, timedelta, timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configurações do Telegram
api_id = '23362895'  # Substitua com sua API ID
api_hash = '9fa49400cb046b4538dacbc62ed78ba7'  # Substitua com seu API hash
phone_number = '558193823723'  # Número de telefone
client = TelegramClient('session_name', api_id, api_hash)

# Configurações da API GitHub
GITHUB_USERNAME = 'GustaavooC'  # Substitua com seu nome de usuário do GitHub
GITHUB_API_URL = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'

# ID do Canal (ou Grupo)
CANAL_ID = -1002265410938  # ID do seu grupo/canal

# Função para salvar e analisar as vagas
def save_vaga_and_post(message):
    # Verificar se a mensagem tem texto e não é None
    if not message.text:
        return  # Se não tiver texto, ignorar a mensagem

    # Verificar se há link na mensagem
    url = extract_url(message.text)
    
    keywords = ['vaga', 'desenvolvedor', 'oportunidade', 'programador', 'TI', 'fullstack', 'remoto', 'PHP', 'Laravel', 'Docker']
    
    # Verificar se a mensagem contém alguma palavra-chave
    if any(keyword in message.text.lower() for keyword in keywords):
        print(f"Vaga encontrada: {message.text}")
        
        # Extrair informações de contato (e-mail e telefone)
        contact_email, contact_phone = extract_contact_info(message.text)
        
        # Enviar para análise
        analysis, compatibility = analyze_vaga_with_github(message.text, url)
        
        # Se a compatibilidade for superior a 60%, adicionar um alerta
        alert = "🚨 **Alerta! Alta compatibilidade com seu perfil!** 🚨\n" if compatibility >= 60 else ""
        
        # Postar a análise no canal junto com a mensagem original
        client.loop.create_task(post_to_channel(message.text, url, analysis, alert, contact_email, contact_phone))

# Função para extrair link da vaga (se presente na mensagem)
def extract_url(text):
    # Verifique se o texto não é None
    if not text:
        return None  # Retorna None se o texto for None ou vazio
    # Regex para encontrar links (URLs)
    urls = re.findall(r'https?://[^\s]+', text)
    return urls[0] if urls else None

# Função para extrair informações de contato (e-mail e telefone)
def extract_contact_info(text):
    # Usar regex para encontrar e-mails
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    email = email.group(0) if email else None
    
    # Usar regex para encontrar números de telefone (formatos comuns)
    phone = re.search(r'(\+?[\d\s-]{10,15})', text)
    phone = phone.group(0) if phone else None
    
    return email, phone

# Função para analisar a vaga com base no perfil do GitHub
def analyze_vaga_with_github(vaga_text, url):
    # Coletando o perfil do GitHub
    repos = requests.get(GITHUB_API_URL).json()
    github_profile = [repo['name'] for repo in repos]
    
    # Palavras-chave extraídas da descrição da vaga
    vaga_keywords = extract_keywords_from_vaga(vaga_text)
    
    # Comparar palavras-chave da vaga com o perfil do GitHub usando TF-IDF e similaridade cosseno
    compatibility_score = predict_compatibility(vaga_keywords, github_profile)
    
    # Criar uma sugestão de melhoria com base na comparação
    improvement_suggestions = generate_suggestions(vaga_keywords, github_profile)

    return improvement_suggestions, compatibility_score

# Função para extrair palavras-chave da descrição da vaga
def extract_keywords_from_vaga(vaga_text):
    # Define as palavras-chave relacionadas à vaga (ex: linguagens, frameworks)
    keywords = ['Python', 'JavaScript', 'PHP', 'Laravel', 'React', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'SQL', 'MongoDB']
    found_keywords = [kw for kw in keywords if kw.lower() in vaga_text.lower()]
    return found_keywords

# Função para calcular a compatibilidade usando TF-IDF e similaridade cosseno
def predict_compatibility(vaga_keywords, github_profile):
    # Unir as palavras-chave da vaga e do perfil do GitHub para análise
    documents = [' '.join(vaga_keywords), ' '.join(github_profile)]
    
    # Usar TF-IDF para transformar os documentos em vetores
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calcular a similaridade cosseno entre os dois documentos
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # A compatibilidade será a similaridade cosseno (em percentual)
    compatibility = cosine_sim[0][0] * 100  # Retorna a compatibilidade como porcentagem
    
    # Garantir que a compatibilidade esteja entre 0 e 100 (caso de erro)
    compatibility_percentage = max(0, min(100, round(compatibility, 2)))  # Arredonda a compatibilidade e limita entre 0 e 100
    
    return compatibility_percentage

# Função para gerar sugestões de melhoria baseadas nas palavras-chave da vaga
def generate_suggestions(vaga_keywords, github_profile):
    suggestions = []
    
    for keyword in vaga_keywords:
        if not any(keyword.lower() in repo.lower() for repo in github_profile):
            suggestions.append(f"Considere adicionar repositórios ou projetos relacionados a '{keyword}' no seu GitHub para aumentar a compatibilidade.")
    
    if not suggestions:
        suggestions.append("Seu perfil já está bem alinhado com as palavras-chave da vaga!")
    
    return "\n".join(suggestions)

# Função para formatar a postagem de forma atrativa com emojis
def format_post(vaga_text, url, analysis, alert="", contact_email=None, contact_phone=None):
    # Exemplo de formatação com emojis e uma boa estrutura
    post = f"""
    {alert}🚀 **Vaga Encontrada!** 📢

    📋 **Descrição da Vaga**:
    {vaga_text}

    🌐 **Link da Vaga**:
    {url}

    🔍 **Análise da Vaga**:
    {analysis}

    📝 **Sugestões de Melhoria**:
    {analysis}

    📨 **Meio de Contato**:
    E-mail: {contact_email if contact_email else 'Não fornecido'}
    Telefone: {contact_phone if contact_phone else 'Não fornecido'}

    📝 **Boa sorte!** Espero que consiga a vaga! 🍀
    """

    return post

# Função para postar a análise no canal
async def post_to_channel(vaga_text, url, analysis, alert="", contact_email=None, contact_phone=None):
    formatted_post = format_post(vaga_text, url, analysis, alert, contact_email, contact_phone)
    await client.send_message(CANAL_ID, formatted_post)

# Função para buscar vagas das últimas semanas
async def fetch_recent_vagas():
    # Definir o intervalo de tempo (últimas 2 semanas, por exemplo)
    date_limit = datetime.now(timezone.utc) - timedelta(weeks=2)
    
    # Coletar as mensagens recentes dos grupos (últimas 2 semanas)
    async for message in client.iter_messages(CANAL_ID, limit=100):
        # Verificar se a mensagem tem a propriedade 'date'
        if hasattr(message, 'date') and message.date > date_limit:  # Filtrar as mensagens que estão dentro do limite de tempo
            save_vaga_and_post(message)

# Evento para escutar as mensagens
@client.on(events.NewMessage())
async def handler(event):
    message = event.message
    save_vaga_and_post(message)

# Função principal
async def main():
    await client.start(phone_number)
    print("Bot iniciado. Coletando vagas das últimas semanas e postando análises no canal...")
    
    # Buscar as vagas das últimas semanas ao iniciar
    await fetch_recent_vagas()
    
    # Continuar executando e ouvindo novas mensagens
    await client.run_until_disconnected()

# Iniciar o cliente
client.loop.run_until_complete(main())
