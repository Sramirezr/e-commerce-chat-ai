#  E-Commerce Chat AI

Proyecto desarrollado como parte del taller de **Construcción de Software**, que implementa un **sistema de chat inteligente** para un e-commerce.  
El asistente virtual está potenciado por **Google Gemini AI**, permitiendo recomendar productos a los usuarios con contexto conversacional.

---

##  Características Principales

- API REST construida con **FastAPI**
- Persistencia de datos con **SQLite y SQLAlchemy**
- Chat con inteligencia artificial usando **Gemini API**
- Arquitectura limpia con 3 capas:
  - **Domain** (entidades y reglas de negocio)
  - **Application** (servicios y casos de uso)
  - **Infrastructure** (API, DB, repositorios e IA)
- Contenerización completa con **Docker y Docker Compose**
- Pruebas unitarias con **Pytest y Pytest-Asyncio**
- Documentación automática en `/docs`
- Totalmente documentado con **docstrings en español (Google Style)**

---

##  Arquitectura del Proyecto

```plaintext
e-commerce-chat-ai/
├── src/
│   ├── domain/
│   │   ├── entities.py
│   │   └── repositories.py
│   ├── application/
│   │   ├── dtos.py
│   │   ├── chat_service.py
│   │   └── product_service.py
│   └── infrastructure/
│       ├── api/
│       │   └── main.py
│       ├── db/
│       │   ├── models.py
│       │   └── database.py
│       ├── repositories/
│       └── llm_providers/
│           └── gemini_service.py
├── data/
├── tests/
├── evidencias/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
