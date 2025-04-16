from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import requests
import random
import datetime

# Configurações da API
API_URL = "http://host.docker.internal:8000/api/eventos/"
TOKEN_URL = "http://host.docker.internal:8000/api/token/"
USERNAME = "airflow_user"
PASSWORD = "@uthomation"


def get_token():
    response = requests.post(TOKEN_URL, json={
        "username": USERNAME,
        "password": PASSWORD
    })
    response.raise_for_status()
    token = response.json().get("access")
    Variable.set("jwt_token", token)
    return token


def gerar_evento():
    status = random.choices(["success", "warning", "error"], weights=[70, 20, 10])[0]
    payload = {
        "titulo": f"Evento gerado - {status}",
        "descricao": f"Simulação automática de evento com status: {status}"
    }

    token = Variable.get("jwt_token", default_var=None)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 401:
        token = get_token()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(API_URL, json=payload, headers=headers)

    response.raise_for_status()
    print(f"[Airflow] Evento enviado: {payload}")


with DAG(
    dag_id="gerador_eventos",
    start_date=days_ago(1),
    schedule_interval="*/2 * * * *",  # Executa a cada 2 minutos
    catchup=False,
    description="Gera eventos aleatórios com sucesso, warning ou erro"
) as dag:

    tarefa_gerar_evento = PythonOperator(
        task_id="gerar_evento",
        python_callable=gerar_evento
    )

    tarefa_gerar_evento