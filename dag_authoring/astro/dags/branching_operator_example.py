# imports
from datetime import datetime
from airflow.decorators import task, dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.models.baseoperator import chain


default_args ={
    "start_date": datetime(2023,1,1)
}

# task defitnition
@task.python
def task_one():

    print("I'm the first")


@task.python
def task_two():

    print("I'm the second")


def _choosing_task_based_on_day(execution_date):
    today_day = execution_date.day_of_week

    if (today_day in (1,2,3)):
        return 'task_one'
    
    elif (today_day in (4,5,6)):
        return 'task_two'
    
    else:
        return 'stop'


# dag definition
@dag(catchup=False, schedule=None, default_args=default_args, max_active_runs=1)
def chooser_dag():

    start = EmptyOperator(task_id="start")
    #end = EmptyOperator(task_id="end")
    end = EmptyOperator(task_id="end", trigger_rule='none_failed_or_skipped')
    stop = EmptyOperator(task_id="stop")

    choosing_task_based_on_day = BranchPythonOperator(
        task_id='choosing_task_based_on_day',
        python_callable=_choosing_task_based_on_day
    )

    start >> choosing_task_based_on_day >> stop
    chain(start, choosing_task_based_on_day, [task_one(), task_two()], end)

dag = chooser_dag()
