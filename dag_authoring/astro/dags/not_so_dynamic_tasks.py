# imports
from datetime import datetime
from airflow.decorators import task, dag
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import chain


default_args ={
    "start_date": datetime(2023,1,1)
}

taxis = {
    "green_cab": {
        "driver_first_name": "Astro",
        "driver_last_name": "Nomer",
        "driver_age": 1
    },
    "yellow_cab": {
        "driver_first_name": "Air",
        "driver_last_name": "Flow",
        "driver_age": 2
    }
}

# task defitnition
@task.python
def printing_info(full_name, age):

    print(f"{full_name['full_name']} has {age} years!")


# dag definition
@dag(catchup=False, schedule=None, default_args=default_args, max_active_runs=1)
def taxi_driver_info():

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    for taxi_cab, driver_info in taxis.items():

        @task.python(task_id=f"formatting_info_{taxi_cab}", multiple_outputs=True)
        def formatting_info(fisrt_name, last_name):
            full_name = fisrt_name + last_name

            return {"full_name": full_name.title()}

        
        driver_name_full_name = formatting_info(
            driver_info['driver_first_name'], 
            driver_info['driver_last_name']
        )

        chain(
            start,
            driver_name_full_name, 
            printing_info(driver_name_full_name, driver_info['driver_age']), 
            end
        )


dag = taxi_driver_info()
