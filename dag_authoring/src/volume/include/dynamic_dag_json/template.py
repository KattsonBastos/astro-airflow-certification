from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(
    f"get_price_json_DAG_ID_HOLDER",
    start_date=datetime(2022,1, 1),
    schedule_interval="SCHEDULE_INTERVAL_HOLDER", 
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
    
    send_email(process(extract(INPUT_HOLDER)))