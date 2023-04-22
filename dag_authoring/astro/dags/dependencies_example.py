# imports
from datetime import datetime
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import cross_downstream, chain

# dag definition
@dag(catchup=False, schedule=None, start_date=datetime(2023,1,1))
def dep_dag():

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    t1 = EmptyOperator(task_id='t1')
    t2 = EmptyOperator(task_id='t2')
    t3 = EmptyOperator(task_id='t3')

    t4 = EmptyOperator(task_id='t4')
    t5 = EmptyOperator(task_id='t5')
    t6 = EmptyOperator(task_id='t6')

    # [t1, t2, t3] >> t4
    # [t1, t2, t3] >> t5
    # [t1, t2, t3] >> t6

    cross_downstream([t1, t2, t3], [t4, t5, t6])
    chain(start, [t1, t2, t3], [t4, t5, t6], end)

dep_dag()