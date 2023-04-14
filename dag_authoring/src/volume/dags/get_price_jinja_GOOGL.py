from airflow import DAG
from airflow.decorators import task

from datetime import datetime

with DAG("get_price_jinja_GOOGL", start_date=datetime(2022,1, 1), 
        schedule_interval="@daily", 
        catchup=False,
        tags = ["dynamic_jinja"]
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