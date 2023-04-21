# imports
from datetime import datetime
from airflow.decorators import task, dag
from airflow.utils.task_group import TaskGroup

from groups.other_printer_gp import printing_info_v2, printing_info_v3

default_args ={
    "start_date": datetime(2023,1,1),
}

@task.python(task_id="getting_info", do_xcom_push=False, multiple_outputs=True)
def getting_info():

    person_name = "Astronomer"

    person_job = "Airflow"

    return {"person_name": person_name, "person_job": person_job}


@task.python#(task_id="printing_name")
def printing_name(person_name):
    
    print('Hi, ', person_name)


@task.python#(task_id="printing_job")
def printing_job(person_job):
    
    print('Your job: ', person_job)


# dag definition
@dag(catchup=False, schedule=None, default_args=default_args)
def tf_dag():

    person_info = getting_info()

    with TaskGroup(group_id="printing_info") as printing_info:

        printing_name(person_info['person_name'])
        printing_job(person_info['person_job'])

    printing_info_v2(person_info)

    printing_info_v3(person_info)


dag = tf_dag()
