# 🌊 Achadinhos Oceano

Sistema desenvolvido em Python com FastAPI para exibir produtos da Shopee utilizando uma estratégia híbrida de consulta (Banco SQLite + API da Shopee).

## ✨ Funcionalidades

- Pesquisa de produtos
- Paginação de 24 produtos por página
- Atualização automática do banco
- Busca híbrida (Banco → API → Banco)
- Interface responsiva
- SEO otimizado
- Integração com programa de afiliados da Shopee

## 🛠 Tecnologias

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- HTML5
- CSS3
- JavaScript

## 📂 Estrutura

```
app/
├── database/
├── services/
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
└── main.py
```

## 🚀 Como executar

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

Windows

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python -m uvicorn app.main:app --reload
```

Abra:

```
http://127.0.0.1:8000
```

## 📌 Status

🟢 Em desenvolvimento.

## 👤 Autor

Carlos