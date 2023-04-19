# The Power of the Taskflow API

[back to dag authoring page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The Taskflow API paradigm was released in the versoin 2.0 of Airflow and brings us a new of of easily write DAGs. So, with fewer lines of code, we have the same pipeline, but, with this, it is easier to <strong>build</strong>, <strong>read</strong>, and <strong>maintain</strong>.
</p>

<a name="readme-top"></a>

<p id="contents"></p>

## Contents
- <a href="#intro">Introduction</a>
- <a href="#templating">Adding data at runtime with templating</a>
- <a href="#tr_xcoms">The Traditional XCOM Way</a>
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
<p id="tf_xcom"></p>
  
## The Taskflow API XCOM Way