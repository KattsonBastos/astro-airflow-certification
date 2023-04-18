# importing libraries

## general libraries
from datetime import datetime, timedelta

## airflow libraries
from airflow.models import Variable
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


@task
def print_variable(received_variable):
    staging_bucket_path = Variable.get("staging_bucket_path")
    print('The Variable is: ', staging_bucket_path)

    user_passwd = Variable.get("user_password")

    print("User's password is:", user_passwd)

    taxi_info = Variable.get("taxi_info", deserialize_json=True)

    print("Taxi info: \n", taxi_info)

    print('Taxi from jinja: ', received_variable)


# declaring dag
default_args = {
	"owner": "Kattson Bastos",
	"retries": 1,
	"retries_delay": 0
}


@dag(
    start_date=datetime(2023,4,6),
    schedule=None,
    max_active_runs=1,
    default_args=default_args,
    catchup=False,
    tags=['template', 'variables']
)
def test_variable():
    init = EmptyOperator(task_id="init")

    end = EmptyOperator(task_id="end")

    received_variable = "{{ var.json.taxi_info }}"

    init >> print_variable(received_variable) >> end


dag = test_variable()
