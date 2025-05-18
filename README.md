# future-minds-ai-na-pratica

Future Minds | AI na Prática

## Requisitos

- Python v3.x e Pip instalados;
- Uma API Key da Open AI: https://platform.openai.com/settings/organization/api-keys
- Um arquivo `.env` com a propriedade `OPENAI_API_KEY`com sua API Key;

## Como executar

Primeiramente crie o arquivo `.env` na raiz do repositório com o seguinte conteúdo:

```properties
OPENAI_API_KEY=<sua-api-key-gerada-na-openai>
```

Em seguida, crie um ambiente virtual local com o Venv (Virtual Environment) para o projeto e instale as dependências:

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Por fim, para executar o script, basta:

```
python3 main.py
```

Após executar o comando acima, uma história (textual) gerada pela AI será impressa no console e também no diretório `./output` com os seguintes arquivos:

1. `{timestamp}-01-historia-text.txt`: história **textual** gerada pela AI a partir do input do usuário;
2. `{timestamp}-02-historia-audio.txt`: história em **aúdio** gerada pela AI a partir da história textual;
3. `{timestamp}-04-historia-image.txt`: história em **imagem** gerada pela AI a partir da história textual;

# Dúvidas e suporte

Basta enviar uma mensagem no Chat da Zup ou enviar um email para rafael.ponte@zup.com.br.
