# The Executors

[back to fundamentals page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;As we saw, Executors defines the way our tasks are going to be executed. There are a lot of options: executors for running tasks on a local machine, on a Kubernetes cluster, and so on. Thus, let's take a look at some of them and at some details in this executors realm.
</p>

<p id="contents"></p>

## Contents 

- <a href="#default">SequentialExecutor: the default</a>
- <a href="#parallel">Parameters to deal with Tasks Parallelism</a>
- <a href="#prod">Executors in Production</a>

---
<p id="default"></p>

## Basic Structure of a DAG

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The SequentialExecutor is the default executor in Airflow right after the installation. Since Airflow comes with sqlite as the default database and sqlite does not support multiple connections, the SequentialEdxecutor is perfect for a default configuratin, since it will only run one task instance at a time. That's also the reason why it is not recommended to be used in production. For instance, if we have two tasks we want to run in parallel,l et's say, data extraction from two different sources, and we're using the SequentialExecutor, one of those task will be executed first and, then, the other. In this way, it is more recommended for task debugging and experimentation purposes.
</p>

---
<p id="parallel"></p>

## Parameters to deal with Tasks Parallelism

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Airflow allows us to specify how many tasks we want to run in parallel. In the following we summarize three important parameters to do so:
</p>

- parallelism (default: 32): defines the number of tasks we can run at the same time in our entire Airflow instance.
- dag_concurrency (default: 16): for a given DAG, it defines the number of tasks that can be executed in parallel across all DAG Runs of that DAG.
- max_active_runs_per_dag (default: 16): defines the number DAG Runs that can be executed in parallel for a given DAG.

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Support we have a dag_concurrency of 16 and a parallelism of 6. How many tasks Airflow will run at the same time, if in case? The answer is 6. Those parameters are applied globally in our Airflow instance.
<br>

&ensp;&ensp;&ensp;&ensp;Those parameters are applied globally in our Airflow instance. So, what if we want to limit the number of parallel DAG Runs for a specific DAG? Well, we just have to pass the value to the max_active_entries in the DAG creation. Also, if we want to limit the number of tasks running in parallel for a specific DAG, we just have to pass the value to the concurrency parameter:
</p>

```python
from airflow import DAG

with DAG(
    dag_id="etl_pipeline",
    start_date=None,
    max_active_entries=2,
    concurrency=1

) as dag:

    extract = Operator(
        task_id='extract'
    )

```

<p id="default"></p>

## Executors in Production

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;What if we want to execute Airflow in production, what Executor should we use? The first option is the LocalExecutor. The LocalExecutor allows us to execute multiple tasks at the same time as long as we have only one machine. According to the
</p>

### LocalExecutor
<p align="justify">
&ensp;&ensp;&ensp;&ensp;The first option is the LocalExecutor. It allows us to execute multiple tasks at the same time as long as we have only one machine. According to <a href="https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html">the docs</a>, whenever our tasks needs to be triggered, it creates subprocesses in the machine to execute the task. To use it, we basically just have to change the Airflow database (such as a Postgres) and change the configuration.
</p>

### Getting things bigger: the CeleryExecutor

<p align="justify">
&ensp;&ensp;&ensp;&ensp;This Executor is a good choice if we need to scale out the number of Workers. Since Celery is a distributed task queue, we can use it to distribute teasks between the Workers. However, to do this job, we need an additional component: a queue. This is basically a third party tool, such as RabbitMQ or Redis, that creates a queue where our tasks will be pushed by the Executor and pulled by the Workers.
<br>

&ensp;&ensp;&ensp;&ensp;An important thing to keep in mind is that once we have multiple machines, multiple workers, we'll need to take care of the dependencies: we'll need Airflow installed in all machines, otherwise a machine won't be able to execute a task; dependencies needed by the DAG, such as a python library or an ODBC driver.
</p>