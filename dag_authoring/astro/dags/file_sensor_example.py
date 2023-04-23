# imports
from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import chain
from airflow.contrib.sensors.file_sensor import FileSensor

@task.python
def print_df():
    import pandas as pd
    print('Hi')



# dag definition
@dag(catchup=False, schedule=None, start_date=datetime(2023,1,1))
def file_sensor_example():

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    sensor_task = FileSensor(
        task_id="file_sensor_task",
        poke_interval= 60,
        filepath="/tmp/tmp_file.csv"
    )


    chain(
        start,
        sensor_task,
        print_df(),
        end
    )

file_sensor_example()