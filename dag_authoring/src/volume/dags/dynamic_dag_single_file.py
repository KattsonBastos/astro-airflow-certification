# Using globals() to dynamically generate DAGs

from airflow import DAG
from airflow.decorators import task
from datetime import datetime

def create_dag(symbol):
    with DAG(
        f'get_price_single_file_{symbol}', 
        start_date=datetime(2022,1, 1), 
        schedule_interval='@daily', 
        catchup=False,
        tags=["dynamic_single"]
    ) as dag:

        @task
        def extract(symbol):
            return symbol


        @task
        def process(symbol):
            return symbol

        @task
        def send_email(symbol):
            print(symbol)
            return symbol

        send_email(process(extract(symbol)))
        
        return dag

for symbol in ("APPL", "FB", "GOOGL"):
    globals()[f"dag_{symbol}"] = create_dag(symbol)