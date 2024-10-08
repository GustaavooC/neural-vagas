

# **NeuralBot - Bot de Análise de Vagas no Telegram** 🤖💼

Olá, eu sou **Gustavo Cavalanti** e este é o projeto **NeuralBot**! 🚀

O **NeuralBot** é um bot para **Telegram** que coleta vagas de emprego postadas em canais e grupos, analisa as tecnologias exigidas e verifica a compatibilidade com os repositórios do GitHub do usuário. Ele usa uma **rede neural simples** para identificar quais habilidades são mais relevantes para a vaga e gera sugestões de como o usuário pode melhorar seu perfil.

[**Meu GitHub**](https://github.com/GustaavooC/)

---

## **Funcionalidades** ⚙️

- **Coleta de Mensagens de Vagas**: O bot escuta as mensagens em um canal ou grupo do Telegram e detecta se a mensagem contém palavras-chave relacionadas a vagas de emprego.
  
- **Extração de Links e Contatos**: Quando uma vaga é identificada, o bot tenta extrair **links** da vaga e informações de **contato** como e-mails ou números de telefone.
  
- **Análise de Compatibilidade com GitHub**: O bot acessa os **repositórios públicos** do GitHub do usuário e compara as tecnologias mencionadas na vaga com os projetos do perfil, utilizando técnicas como **TF-IDF** e **similaridade cosseno**.

- **Sugestões de Melhoria**: Se o bot encontrar tecnologias na vaga que não estão presentes no perfil do GitHub, ele sugere que o usuário adicione repositórios relacionados às tecnologias mencionadas.

- **Postagem de Resultados**: O bot envia os resultados da análise diretamente no canal ou grupo, com informações detalhadas sobre a vaga, compatibilidade e sugestões.

---

## **Tecnologias Utilizadas** 💻

- **Python 3.x**
- **Telethon**: Para interação com a API do Telegram.
- **Scikit-learn**: Para análise de texto com **TF-IDF** e **similaridade cosseno**.
- **Requests**: Para fazer requisições à API do GitHub.
- **Expressões Regulares (Regex)**: Para extração de links e contatos.

---

## **Instalação** 🛠️

1. Clone este repositório:

```bash
git clone https://github.com/GustaavooC/neural-vagas.git
cd VagaBot
```

2. Crie e ative um ambiente virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis no código:
   - **API ID e API Hash** do Telegram (obtidos em [Telegram API](https://my.telegram.org/auth)).
   - **Número de telefone** para login no Telegram.
   - **Nome de usuário do GitHub** para coletar repositórios.
   - **ID do Canal ou Grupo** para onde as vagas serão postadas.

---

## **Como Usar** 🚀

1. Execute o script principal:

```bash
python main.py
```

2. O bot começará a escutar as mensagens do canal ou grupo especificado. Quando uma nova vaga for detectada, ele fará a análise e enviará os resultados para o canal.

---

## **Exemplo de Postagem** 📩

Aqui está um exemplo de como a mensagem será formatada no canal:

```
🚀 **Vaga Encontrada!** 📢

📋 **Descrição da Vaga**:
Desenvolvedor Fullstack com experiência em Laravel, PHP, Docker e AWS.

🌐 **Link da Vaga**:
https://link-da-vaga.com

🔍 **Análise da Vaga**:
Compatibilidade com seu perfil: 75%

📝 **Sugestões de Melhoria**:
Considere adicionar repositórios sobre Docker e AWS no seu GitHub.

📨 **Meio de Contato**:
E-mail: exemplo@email.com
Telefone: +55 1234567890

📝 **Boa sorte!** Espero que consiga a vaga! 🍀
```

---

## **Contribuição** 🤝

Sinta-se à vontade para contribuir com melhorias! Você pode:

1. Fazer um **fork** do repositório.
2. Criar uma **branch** com suas alterações.
3. Enviar um **pull request**.

---

## **Licença** 📜

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Gustavo Cavalanti**  
[GitHub](https://github.com/GustaavooC/) | [LinkedIn](https://www.linkedin.com/in/gustavocavalanti/)
```


