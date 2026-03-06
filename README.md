# 📸 Instagram Profile Picture Scraper

API para capturar fotos de perfil do Instagram via automação com Playwright + FastAPI.

## 🚀 Como funciona

1. Acessa o perfil do Instagram via Chromium headless
2. Extrai o parâmetro `oe` da meta tag `og:image` do HTML
3. Cruza com as requisições interceptadas que possuem o mesmo `oe`
4. Retorna a URL exata da foto de perfil

## 📁 Estrutura

```
.
├── Dockerfile
├── main.py
└── README.md
```

## 📡 Uso da API

### `GET /foto`

**Parâmetros**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `usernames` | string | Um ou mais @ separados por vírgula |

**Exemplo de requisição**
```
GET http://localhost:8000/foto?usernames=conta1,conta2
```

**Exemplo de resposta**
```json
{
  "conta1": "https://instagram.fbsb25-1.fna.fbcdn.net/v/t51.2885-19/...",
  "conta2": "https://instagram.fbsb25-1.fna.fbcdn.net/v/t51.2885-19/..."
}
```

> ⚠️ As URLs possuem expiração. Baixe ou processe a imagem logo após receber a resposta.

## 🛠️ Tecnologias

- [Python 3.12](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Playwright](https://playwright.dev/python/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)
