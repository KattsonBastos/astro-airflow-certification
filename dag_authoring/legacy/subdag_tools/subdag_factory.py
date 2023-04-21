from airflow.models import DAG
from airflow.decorators import task
from airflow.operators.python import get_current_context

@task.python
def task_one():
    ti = get_current_context()['ti']

    person_name = ti.xcom_pull(key='return_value', task_ids='task_zero', dag_id='my_dag')
    
    print('Hi, ', person_name)



def subdag_factory(parent_dag_id, subdag_dag_id, default_args):
    with DAG(f"{parent_dag_id}.{subdag_dag_id}", default_args=default_args) as dag:

        task_one()
    
    return dag
