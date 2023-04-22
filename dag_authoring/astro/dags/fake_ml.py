# imports
from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import cross_downstream, chain


@task.python(pool="ml_model_training")
def train_model_1():
    import time
    time.sleep(30)


@task.python(pool="ml_model_training")
def train_model_2():
    import time
    time.sleep(30)


@task.python(pool="ml_model_training")
def train_model_3():
    import time
    time.sleep(30)


@task.python
def test_model_1():
    import time
    time.sleep(30)


@task.python
def test_model_2():
    import time
    time.sleep(30)


@task.python
def test_model_3():
    import time
    time.sleep(30)


# dag definition
@dag(catchup=False, schedule=None, start_date=datetime(2023,1,1))
def fake_ml():

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')


    chain(start, [train_model_1(), train_model_2(), train_model_3()], [test_model_1(), test_model_2(), test_model_3()], end)

fake_ml()