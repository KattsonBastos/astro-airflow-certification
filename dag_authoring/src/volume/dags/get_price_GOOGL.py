from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(
    f"get_price_json_GOOGL",
    start_date=datetime(2022,1, 1),
    schedule_interval="@daily", 
    catchup=False,
    tags=["dynamic_json"]
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
    
    send_email(process(extract(3243)))