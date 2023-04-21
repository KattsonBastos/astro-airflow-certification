# imports
from airflow.decorators import task, dag
from airflow.utils.task_group import TaskGroup


@task.python#(task_id="printing_name")
def printing_name(person_name):
    
    print('Hi, ', person_name)


@task.python#(task_id="printing_job")
def printing_job(person_job):
    
    print('Your job: ', person_job)


@task.python#(task_id="printing_name")
def formatting_name():
    
    print('Formatting person name')


@task.python#(task_id="printing_job")
def formatting_job():
    
    print('Formatting person job')


def printing_info_v2(person_info):
    with TaskGroup(group_id="printing_info_v2") as printing_info_v2:

        printing_name(person_info['person_name'])
        printing_job(person_info['person_job'])

    
    return printing_info_v2


def printing_info_v3(person_info):
    with TaskGroup(group_id="printing_info_v3") as printing_info_v3:

        with TaskGroup(group_id="formatting_info") as formatting_info:
            formatting_name()
            formatting_job()

        printing_name(person_info['person_name']) >> formatting_info
        printing_job(person_info['person_job']) >> formatting_info

    return printing_info_v3