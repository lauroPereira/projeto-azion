from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def tarefa_simples():
    print("Executando tarefa simples!")

with DAG(
    dag_id="dag_teste_simples",
    start_date=datetime(2025, 4, 4),
    schedule_interval="@once",  # executa apenas uma vez
    catchup=False,
) as dag:
    tarefa = PythonOperator(
        task_id="executar_tarefa",
        python_callable=tarefa_simples,
    )
