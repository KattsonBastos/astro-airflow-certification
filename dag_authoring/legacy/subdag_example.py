# imports
from datetime import datetime
from airflow.operators.subdag import SubDagOperator
from subdag_tools.subdag_factory import subdag_factory
from airflow.decorators import task, dag

default_args ={
    "start_date": datetime(2023,1,1),
}

@task.python(task_id="task_one")
def task_zero():

    person_name = "Astronomer"

    return person_name


# dag definition
@dag(catchup=False, schedule=None, default_args=default_args)
def my_dag():

    saying_hello = SubDagOperator(
        task_id="saying_hello",
        subdag=subdag_factory("my_dag", "saying_hello", default_args)
    )

    task_zero() >> saying_hello


dag = my_dag()

