# 📡 EventStream – Real-Time Event Processing with Django, RabbitMQ & Airflow
EventStream é uma POC prática e educativa para demonstrar conceitos modernos de engenharia de software e dados, utilizando Django, Celery, RabbitMQ e Apache Airflow.

## 🎯 Objetivo do Projeto
O projeto simula um fluxo completo de processamento de eventos:
- Geração automática de eventos via Airflow (DAG periódica).
- Armazenamento dos eventos em banco de dados PostgreSQL.
- Encaminhamento assíncrono via fila RabbitMQ usando Celery.
- Processamento distribuído por workers especializados.
- Exposição via API REST e GraphQL.


## ⚙️ Arquitetura Geral
```
            ┌───────────────┐
            │ Apache Airflow│
            └──────┬────────┘
                   │
                   ▼
        ┌────────────────────┐
        │ Django REST API    │◄───── Auth via JWT
        └──────┬─────────────┘
               │
          ┌─────▼───────┐
    ┌────>│ PostgreSQL  │<───────────────┐
    │     └──────┬──────┘                │
    │            │                       │
    │     ┌──────▼────────────┐          │
    │     │ Celery Dispatcher │          │
    │     └──────┬──────┬─────┘          │
    │            │      │                │
    │ ┌──────────▼─┐  ┌─▼──────────────┐ │
    │ │ Worker 1   │  │ Worker 2       │─┘      ┌──────┐
    └─│ (warning)  │  │ (error + email)│───────>│ SMPT │
      └────────────┘  └────────────────┘        └──────┘
```

## 🛠️ Tech Stack
- Python + Django – API REST e backend principal
- PostgreSQL – Armazenamento transacional
- Celery – Workers assíncronos
- RabbitMQ – Message broker
- Graphene (GraphQL) – API para queries analíticas
- Apache Airflow – Orquestrador de jobs
- Docker Compose – Infraestrutura local
- JWT (SimpleJWT) – Autenticação segura

## 🚀 Quick Start
1. Pré-requisitos
    - Python 3.12
    - Docker + Docker Compose
    - RabbitMQ, PostgreSQL

2. Configuração do .env
Crie um arquivo .env com:
    ```
    SECRET_KEY=chave_secreta
    DEBUG=True

    DB_NAME=eventosdb
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost
    DB_PORT=5432
    CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
    CELERY_RESULT_BACKEND=rpc://
    ```

3. Subir serviços com Docker
    ```bash
    cd eventos_api
    docker-compose -f docker-compose.db.yml up -d
    ```

    Esse comando sobe:
    - Banco PostgreSQL
    - RabbitMQ com UI: http://localhost:15672

4. Ativar ambiente virtual e instalar dependências
    ```python
    python -m venv venv
    source venv/Scripts/activate  # ou source venv/bin/activate no Linux/macOS
    pip install -r requirements.txt
    ```
5. Aplicar as migrações e criar usuário
    ```python
    python manage.py migrate
    python manage.py createsuperuser
    ```

6. Iniciar o servidor Django
    ```python
    python manage.py runserver
    ```
    A API estará disponível em: http://localhost:8000/api/

7. Iniciar os Workers
    ### Worker dispatcher (local)
    ```
    celery -A eventos_api worker -l info -Q celery
    ```

    ### Worker especializado (warning)
    ```
    celery -A eventos_api worker -l info -Q warning_queue
    ```

    ### Worker especializado (error)
    ```
    celery -A eventos_api worker -l info -Q error_queue
    ```

8. Subir o Airflow
    ```
    cd airflow
    docker-compose up -d
    ```
    Acesse o painel: http://localhost:8080 (usuário/senha padrão: airflow / airflow)

## ✅ Funcionalidades implementadas
- DAG gerador_eventos gera eventos com status aleatório.
- Os eventos são armazenados via API Django protegida por JWT.
- Os eventos com status "warning" e "error" são processados por workers distintos.
- Os eventos "error" disparam envio de e-mail simulado.
- Fila celery atua como dispatcher para as filas especializadas.

## 📌 Observações
- **O Airflow usa host.docker.internal para se comunicar com o host (funciona em Docker Desktop Windows/macOS).**
- **O processamento assíncrono usa filas separadas para desacoplamento total.**
- **Os workers podem ser escalados de forma independente.**

## 📫 Contribuições
Pull Requests e ideias são bem-vindas! Essa POC é ótima para treinar conceitos como:
- Arquitetura orientada a eventos
- Mensageria assíncrona
- Monitoramento de workflows com DAGs
- Segregação de responsabilidades por workers