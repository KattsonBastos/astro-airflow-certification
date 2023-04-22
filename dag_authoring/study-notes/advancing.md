# Advanced Concepts

[back to dag authoring page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Sometime we'll have a DAG with a lot of tasks that, for the same input, they do the same thing. For example, for three databases, we'll load the data, make some transformations and, then, load into a DW. Will we have to create one different operator for each task of each database? Actually, there's no need for that. In this section we'll see how to better approach this solution.
</p>

<a name="readme-top"></a>

<p id="contents"></p>

## Contents
- <a href="#dynamic_tasks">Not So Dynamic DAGs</a>
- <a href="#branching">Branching Operator: choosing between tasks</a>

---
<p id="dynamic_tasks"></p>
  
## Not So Dynamic DAGs

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Even though nowadays Airflow has a more sofisticated way of creating tasks dynamically, for this certification we're going to take a look at a simples way: iterating over a dictionary and creating the tasks. Let's better understand that. Suppose we want to create the following DAG:
</p>

<p align='center'>
<img src="../images/dynamic_tasks.png" alt="drawing" width="70%"/>
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Basically, we have taxi driver info, such as name, last name, and age, and we want to create a pipeline that reads that data, formats them and then prints them. The thing is that we want to do that for green and yellow taxi drivers. Usually, we could implement 4 operators, 2 per cab. However, there's no need for that. Let's first take a look at what DAG we could create. You can check the DAG file <a href="https://github.com/KattsonBastos/astro-airflow-certification/blob/main/dag_authoring/astro/dags/not_so_dynamic_tasks.py
">here</a>.
<br>
&ensp;&ensp;&ensp;&ensp;The first thing we'll need is a dictionary. Consider the following:
</p>

```python
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

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Here we could have any configuration we wanted. For simplicity, we considered just one driver info per cab.
<br>
&ensp;&ensp;&ensp;&ensp;The next step is to define the tasks and the DAG. We'll have two tasks:
</p>

```python
# task defitnition
@task.python(task_id=f"formatting_info_{taxi_cab}", multiple_outputs=True)
    def formatting_info(fisrt_name, last_name):
        full_name = fisrt_name + last_name

        return {"full_name": full_name.title()}


@task.python
def printing_info(full_name, age):

    print(f"{full_name['full_name']} has {age} years!")

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The first task receives driver's first and last name, then concat them, and, finally, returns it. The second task only prints that concatenated name and the drivers's age. you can notice in the referenced file that the first task is inside the for loop in the DAG. That's because we wanted to create a specific ID for the formatting task. in order to differenciate.
</p>

```python
# dag definition
@dag(catchup=False, schedule=None, default_args=default_args, max_active_runs=1)
def taxi_driver_info():

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    for taxi_cab, driver_info in taxis.items():
        
        #formatting task
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

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;That's it. The general idea of creating dynamic tasks is as simple as that. One thing we have to keep in mind is that Airflow only create dynamic tasks if it already knows whats the input (the dictionary). That is, it can't create tasks dynamically from the output of another task. That's because we're calling it <strong>not so dynamic</strong> (latest versions have a more sophisticated way of doing this).
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<p id="branching"></p>
  
## Branching Operators: choosing between tasks

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Branching allows us to choose between tasks according to some condition we specify. There are a lot of branching operators
</p>

- **BranchPythonOperator**: choosing a task according the task_id returned by a python function.
- **BranchSQLOperator**: choosing a task according to a value in a SQL table.
- **BranchDateTimeOperator**: choosing a task according to given timeframes.
- **BranchDayOfWeekOperator**: choosing a task according to the current date.

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this section, we'll briefly look at the BranchPythonOperator. Take a look at the following graph:
</p>

<p align='center'>
<img src="../images/branching.png" alt="drawing" width="60%"/>
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Basically, it will execute task_one on mondays, tuesdays, and wednesdays; task_two on thursdays, fridays, and saturdays; otherwise, it stopps. You can find the entire code <a href="https://github.com/KattsonBastos/astro-airflow-certification/blob/main/dag_authoring/astro/dags/branching_operator_example.py
">here</a>. First, we implemented the tasks and the conditioning function:
</p>

```python
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

```

<p>
&ensp;&ensp;&ensp;&ensp;In this case, we're branching based on the execution date. Then, we are able to implement the DAG. Notice that just by returning the task id it automatically choose the corresponding task for us.
</p>

```python
# dag definition
@dag(catchup=False, schedule=None, default_args=default_args, max_active_runs=1)
def chooser_dag():

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    stop = EmptyOperator(task_id="stop")

    choosing_task_based_on_day = BranchPythonOperator(
        task_id='choosing_task_based_on_day',
        python_callable=_choosing_task_based_on_day
    )

    start >> choosing_task_based_on_day >> stop
    chain(start, choosing_task_based_on_day, [task_one(), task_two()], end)

dag = chooser_dag()

```

<p>
&ensp;&ensp;&ensp;&ensp;So beautiful, isn't it? So, let's execute the DAG. After some seconds, we'll see the following:
</p>

<p align='center'>
<img src="../images/branching_skipped.png" alt="drawing" width="60%"/>
</p>

<p>
&ensp;&ensp;&ensp;&ensp;😯 It skipped the 'end' task, even though the task_two was succesfully executed. But, why? 🤔
<br>
&ensp;&ensp;&ensp;&ensp;That's where the concept of Trigger Rules comes into place. Well, a task is ging to be executed based on upstream execution status. So, we can choose to execute a task whether the upstream skipped, failed, succeed, and so on. In order to fix our code and execute the 'end' task in case task_one or task_two have succeedded, we have to add the following argument to the task:
</p>

```python
#end = EmptyOperator(task_id="end")
end = EmptyOperator(task_id="end", trigger_rule='none_failed_or_skipped')

```

<p align='center'>
<img src="../images/branching_success.png" alt="drawing" width="60%"/>
</p>

<p>
&ensp;&ensp;&ensp;&ensp;Now we have the desired output.
</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>
