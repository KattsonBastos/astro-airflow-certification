# Playing with DAGs and Tasks: code details

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this section we're going to take a little look at some DAG Python code, addressing some scheduling and dates concepts, operators, and data exchange between tasks.
</p>

<p id="contents"></p>

## Contents 

- <a href="#struct">Basic Structure of a DAG</a>
- <a href="#dates">Start Date and Scheduling Interval</a>
- <a href="#bf">Backfilling</a>
- <a href="#ops">Some Important Operators</a>
- <a href="#excg">Exchanging Data Between Tasks</a>

---
<p id="struct"></p>

## Basic Structure of a DAG

[back to contents](#contents)


<p align="justify">
&ensp;&ensp;&ensp;&ensp;The first thing we have to do is to create a file which will contain our DAG. Once created in the right folder (as we saw before), we are able to start coding our pipeline. However, there are some different ways to instantiate our DAG and its tasks. Let's take a look at them.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Imagine we want to create a simple ETL pipeline. In this case, we'll have to perform at least three tasks: extract the data, transform the data, and load the data.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;To do so, we can create our DAG in two different ways. THe snippet above shows the first one:
</p>

```python
from airflow import DAG

# instantiating the DAG
dag = DAG(...) # inside the parentheses will come the parameters

# task 1
extract = Operator(dag=dag, ...)

# task 3
transform = Operator(dag=dag, ...)

# task 3
load = Operator(dag=dag, ...)

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this code, we instantiated our DAG by creating the dag object and then, when creating the tasks, we passed that object as an argument to the dag parameters (in this case, our object has the same name, but it could be any other).
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;However, there is a better and cleaner way to instantiate our DAG objects:
</p>


```python
from airflow import DAG

with DAG(dag_id="etl_pipeline") as dag:
    extract = Operator(...)
    transform = Operator(...)
    load = Operator(...)

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Now it is clear that all tasks belong to the DAG. Since it brings a more clean code, we'll keep instantiating DAGs in this way in the following.
</p>


<p align="justify">
&ensp;&ensp;&ensp;&ensp;In order to actually create a (runnable) DAG, we need to put some parameters to those classes. The first one (an extremely important one) is the <strong>dag_id</strong>. The dag_id is a unique (across all of our DAGs) identifier of our DAG. The id, usually a String, is the id we'll be able to identify the task in the UI.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In the following sections we'll take a look at some other important parameters.
</p>



---
<p id="dates"></p>

## Start Date, Execution Date, Scheduling Interval, and End Date

[back to contents](#contents)


<p align="justify">
&ensp;&ensp;&ensp;&ensp;Two of the most important parameters to set up our DAG is the initial date it starts being scheduled and the time interval at which it gets triggered. Let's take a little look on them, but first let's imagine we want to run a daily ETL pipeline and this run will start at 2023/01/01 00:00.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The start date can be any date in the past or in the future. Basically, we can think of it as the initial date of the data interval we want to process in our pipeline. Taking our above example, the start date is 2023/01/01 00:00.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The scheduling interval defines the interval at which our DAGs gets (in our example, a 24h interval). The interval can be in seconds, minutes, hours, and so on. A DAG may or may not have a scheduling interval.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The thing is that Airflow won't trigger our dag at the start date, but only when the start date plus the scheduling interval have elapsed. So, if our start date is setted to 2023/01/01 00:00 and we setted a daily interval, our DAG is effectively triggered at 2023/01/02 00:00 (one day elapsed) and then it will process all data from the start date.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Finally, the End Date is used to pass a date we don't want to trigger our DAG anymore after it.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Until now we saw the concepts, but let's take a look at the code level.
</p>

### Start date in code

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In Airflow we can specify a start date both in the DAG level or in a task (operator) level. If we apply in the DAG, it will be applying to all tasks (operators) in the DAG. However, specifying it directly in the task is not a common use since we can have an execution mess between the tasks dates.
<br>

&ensp;&ensp;&ensp;&ensp;In order to pass a date in Airflow DAG, we need a datetime object. So, we just have to import the built in python datetime object and pass a datetime to the start_date DAG's parameter:
</p>

```python
from airflow import DAG

from datetime import datetime

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2023,1,1)
) as dag:

    extract = Operator(
        task_id='extract'
    )

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;By default, all dates in Airflow is stored in UTC, which is recommended since it can avoid timezones problems. So, it's up to us to manage the timing in order to start scheduling our DAGs in the desired datetime.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;There still are two important things to to keep in mind. First, by default, if we specify a start date in the past, Airflow will trigger all runs between that date and the current date. In order to deal with this behavior, we have to specify some parameters (we'll see them in the next section).
<br>

&ensp;&ensp;&ensp;&ensp;Secondly, it is recommended to set a fixed start date time intead of a dinamically one (it is not a good idea to use datetime.now()). That's because, as we saw before, the DAG is triggered only when the start_date + scheduling_interval has elapsed. It turns out that if we use datetime.now(), the start_date constantly changes and, then, the time to trigger the DAG never comes. SO, we end up with a DAG that never get triggered.
</p>


### Scheduling interval in code


<p align="justify">
&ensp;&ensp;&ensp;&ensp;The scheduling interval is as easier as the start date to be specified: we just have to pass the value to the schedule_interval. This value can be both a cron expression or a timedelta python object. Airflow already brings us some pre defined crons. The image bellow shows some Airflow's 'preset' crons as long as its respective cron tab expression.
</p>

<img src="../images/presets.png" alt="drawing" width="100%"/>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;So, if we want to specify a daily trigger to our DAG, we jsut have to do the following:
</p>


```python
from airflow import DAG

from datetime import datetime

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2023,1,1),
    schedule_interval='@daily'
) as dag:

    extract = Operator(
        task_id='extract'
    )

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;If we want to use timedelta instead of a cron expresson, we can simply pass it as argument:
</p>

```python
from airflow import DAG

from datetime import datetime

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2023,1,1),
    schedule_interval=timedelta(days=1)
) as dag:

    extract = Operator(
        task_id='extract'
    )

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;But what's the difference between cron and timedelta? Well, cron expressions are absolute. That means if we specify that we want to run our dag at 10 AM, it will be triggered at 10 AM. The timedelta is relative: if we specify we want to run our DAG with a timedelta(hours=10), it will be triggered every 10 hours starting from the previsous execution date.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The last thing to keep in mind about the Airflow Scheduling Interval is the ability to pass a None value to the parameters. By doing so, our DAG will never be automatically triggered by the Scheduler, it will be triggered or manually or by an external application.
</p>


---
<p id="bf"></p>

## Backfilling

[back to contents](#contents)


---
<p id="ops"></p>

## Some Important Operators

[back to contents](#contents)

---
<p id="excg"></p>

## Exchanging Data Between Tasks

[back to contents](#contents)