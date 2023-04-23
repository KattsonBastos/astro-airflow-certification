# The Power of the Taskflow API

[back to dag authoring page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/dag_authoring)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The Taskflow API paradigm was released in the versoin 2.0 of Airflow and brings us a new of of easily write DAGs. So, with fewer lines of code, we have the same pipeline, but, with this, it is easier to <strong>build</strong>, <strong>read</strong>, and <strong>maintain</strong>.
</p>

<a name="readme-top"></a>

<p id="contents"></p>

## Contents
- <a href="#intro">Introduction</a>
- <a href="#templating">Adding data at runtime with templating</a>
- <a href="#tr_xcoms">The Traditional XCOM Way</a>
- <a href="#decorators">Decorators: the new way of creating DAGs</a>
- <a href="#tf_xcoms">The Taskflow API XCOM Way</a>

---
<p id="intro"></p>
  
## Introduction

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The Taskflow AP,as we early said, makes DAG authoring easier without extra effort. It also brings another facility: now it's easier to share data between tasks, without needing to pull and push XCOMs. The API has three main aspects. They are:
</p>

1. **XCOM Args**: now the result of a python function task is inferred and automatically passed as a XCOM.
2. **Decorators**: automatically create tasks for a given operator, let's say, PythonOperator.
3. **XCOM Backend**: allows us to store XCOMs in another database than the Airflow metadatabase.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
<p id="templating"></p>
  
## Adding data at runtime with Template Engine

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Airflow's operators have parameters that are or are not templated with the Template Engine, it will depends on each one (to check this, we need to see the docs of each operator). That is,  by default, we are able to pass data to an operator using the jinja template only if it is able to receive that. Let's see an example. Let's see an example.
<br>
&ensp;&ensp;&ensp;&ensp;Let's imagine we're using the Postgres operator to make an operation in the database and we need to filter the only the data of the DagRun execution date. Well, the referred operator allows us to do this:
</p>

```python
fetching_data = PostgresOperator(
    task_id="fetching_data",
    sql="SELECT cab, driver_name FROM ny_taxis WHERE data={{ ds }}"
)

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;What if we wanted to follow best practices and store the sql statement in a separate file, in order to make the DAG cleaner and more readable? Well, the PostgressOperator allows us to pass a file with a SQL statement, what we don't know is whether it allows or not to template the file. By checking the docs, you'll see that we can in fact template a .sql file. Let's imagine we save the above query in a file inside a folder, let's say, 'sql/DRIVER_INFO.sql':
</p>

```python
fetching_data = PostgresOperator(
    task_id="fetching_data",
    sql="sql/DRIVER_INFO.sql"
)

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this way, the task will work the same as before. So far so goo, but what if for some reason we wanted to template a non-templated parameters, what should we do? Is it possible? the answer is: yes. To do that we basically have to create a custom operator. Let's take a non-templated PostgresOperator parameter. PostgresOperator has an optional parameter called 'parameters' that is not templated.
</p>


```python

class CustomPostgresOperator(PostgresOperator):
    
    template_fields = ('sql', 'parameters')


@dag()
def fetch_taxi_data(...):
    fetching_data = CustomPostgresOperator(
        task_id="fetching_data",
        sql="sql/DRIVER_INFO.sql",
        parameters={
            'next_ds': '{{ next_df }}',
            'staging_bucket_path': '{{ var.json.taxi.taxi_staging_bucket }}'
        }
    )

```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
<p id="tr_xcom"></p>
  
## The Traditional XCOM Way

<p align="justify">
&ensp;&ensp;&ensp;&ensp;XCOMs allows us to share data between tasks, such as a file path of an object and they're saved in the metadatabase by default. Even though they really come in handy, XCOMs have some limitations. There are a lot of ways to share XCOMs between tasks, let's see some examples.
<br>
&ensp;&ensp;&ensp;&ensp;The first way is by using the DagRun task_instance variable, as shows the following snippet:
</p>


```python
def task_one(ti):
    ti.xcom_push(key="bucket_path", value="gs://taxi_staging_bucket")


def task_two():
    bucket_name = ti.xcom_pull(key="bucket_path", task_id="task_one")

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The task_one receives the task_instance as an argument and it allows us to pull and push xcom messages. By using the 'xcom_push', the key-pair is pushed. Then, the second task is able to pull that message. The only two parameters we have to pass to get the result is the message key and the task_id that pushed it.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Now we could wonder: ooh, that's pretty amazing. Can I share my pandas dataframe with this? It is not recommended, specially if our dataframe is too big. XCOMs are limited in sizes, and this limitation depends on the metadatabase. So, for a given XCOM, the limits are:
</p>

- **SQLite**: 2GB
- **Postgres**: 1GB
- **MySQL**: 64KB

<p align="justify">
&ensp;&ensp;&ensp;&ensp;There's a cleaner way of pushing XCOMs: just return the value. The difference is that by doing this way it creates a XCOMs with a default key name: return_value. A good thing is that in this case it is optional to use or not the key, as show the following task two and three (both work):
</p>

```python
def task_one(ti):
    return "taxi_staging_bucket"


def task_two():
    bucket_name = ti.xcom_pull(key="return_value", task_id="task_one")


def task_two():
    bucket_name = ti.xcom_pull(task_id="task_one")


```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;What if we want to return multiple values? It's pretty simple, we just have to return a dictionary instead of pushing XCOMs twice. When pulled, we'll get a dictionary:
</p>


```python
def task_one(ti):
    return {"bucket_path":"taxi_staging_bucket", "taxi_cab":"green"}


def task_two():
    bucket_settings = ti.xcom_pull(task_id="task_one")


```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



---
<p id="decorators"></p>

## Decorators: the new way of creating DAGs

<p align="justify">
&ensp;&ensp;&ensp;&ensp;With the new Taskflow API decorators, we have a new way of creating DAGs, tasks, and groups of tasks. In this section we'll take a look at how to create DAG and tasks using the decorators and what is its difference from the traditional way.
<br>
&ensp;&ensp;&ensp;&ensp;Let's consider the following DAG example:
</p>


```python
# imports
[...]  # collapsed for simplicity

# python tasks definition
def _task_one():
    print('Hey')


# dag definition
with DAG(...) as dag:
    first_task = PythonOperator(
        task_id='first_task',
        python_callable=_task_one
    )

    first_task

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In order to start using the Taskflow decorators, we need first to import it. Then, let's create a second task and decorate it:
</p>

```python
# imports
from airflow.decorators import task
[...]  # collapsed for simplicity

# python tasks definition
@task.python
def task_one():
    print('Hey')


# dag definition
with DAG(...) as dag:

    first_task()

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;As simple as that. To update the code to use the DAG operator is also simple. As you'll see, we also have to call the dag function at the end:
</p>

```python
# imports
from airflow.decorators import task
[...]  # collapsed for simplicity

# python tasks definition
@task.python
def task_one():
    print('Hey')


# dag definition
@dag(...)
def my_dag():

    first_task()

dag = my_dag()

```


<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this case, without any other parameter in the task decorator, the function, the name of the function become the task name.
</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>


---
<p id="tf_xcom"></p>
  
## The Taskflow API XCOM Way

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Once we have the new way of creating tasks with the decorator, the way we can create XCOMs also changed. Instead of pushing and pulling XCOMs, Taskflow API makes it easier: 
</p>

```python
# imports
from airflow.decorators import task
[...]  # collapsed for simplicity


@task.python
def task_one():
    
    file_name = "green_taxi_data.csv"

    return file_name


@task.python
def task_two(file_name):
    
    print(file_name)


# dag definition
@dag(...)
def my_dag():

    task_two(task_one())

dag = my_dag()

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Did you notice the difference? Now, we can still kep return the value we want, but, to pull it in the next task, there no need to use the xcom_pull, we can just receive as a parameters and pass the first task as an argument to the second. By doing this way, the XCOM is automatically pushed and pulled and also the dependencies between the two tasks is automatically created.
<br>
&ensp;&ensp;&ensp;&ensp;What if we have multiple messages to share between the tasks? In the traditoinal way, we return a dicionary with multiple key-value pairs, but they are stored as a single message. What if we need to return two values as two different XCOMs, in the same task?
</p>

```python
# imports
from airflow.decorators import task
[...]  # collapsed for simplicity


@task.python(task_id="get_bucket_file_names", multiple_outputs=True)
def task_one():
    
    green_file_path = "green_taxi_data.csv"
    yellow_file_path = "yellow_taxi_data.csv"

    return {"yellow_taxi_path": green_file_path, "green_taxi_path": yellow_file_path}


@task.python
def task_two(yellow_path, green_path):
    
    print(yellow_path, green_path)


# dag definition
@dag(...)
def my_dag():

    taxi_file_path = task_one()

    task_two(taxi_file_path['yellow_taxi_path'], taxi_file_path['green_taxi_path'])

dag = my_dag()

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;This automatically creates two XCOMs, one called yellow_taxi_path and another called green_taxi_path. However, there is another way of doing the same, just by specifying the output of the functoin:
</p>

```python
# imports
from airflow.decorators import task
from tipyng import Dict
[...]  # collapsed for simplicity


@task.python(task_id="get_bucket_file_names")
def task_one() -> Dict([str, str]):
    
    green_file_path = "green_taxi_data.csv"
    yellow_file_path = "yellow_taxi_data.csv"

    return {"yellow_taxi_path": green_file_path, "green_taxi_path": yellow_file_path}


@task.python
def task_two(yellow_path, green_path):
    
    print(yellow_path, green_path)


# dag definition
@dag(...)
def my_dag():

    taxi_file_path = task_one()

    task_two(taxi_file_path['yellow_taxi_path'], taxi_file_path['green_taxi_path'])

dag = my_dag()

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;TThis way still pushes a third XCOM message containing a non separated dictionary of the variables. In order to avoid this, we only have to set another parameters to the decorator: 
</p>

```do_xcom_push=False```

<p align="right">(<a href="#readme-top">back to top</a>)</p>