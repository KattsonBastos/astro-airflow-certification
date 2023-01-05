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

## Start Date and Scheduling Interval

[back to contents](#contents)


<p align="justify">
&ensp;&ensp;&ensp;&ensp;Two of the most important parameters to set up our DAG is the initial date it starts being scheduled and the time interval at which it gets triggered. Let's take a little look on them, but first let's imagine we want to run a daily ETL pipeline and this run will start at 2023/01/01 00:00.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The start date can be any date in the past or in the future. Basically, we can think of it as the initial date of the data interval we want to process in our pipeline. Taking our above example, the start date is 2023/01/01 00:00. It is recommended to set a fixed start date time (it is not a good idea to use datetime.now()).
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The scheduling interval defines the interval at which our DAGs gets (in our example, a 24h interval). The interval can be in seconds, minutes, hours, and so on.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The thing is that Airflow won't trigger our dag at the start date, but only when the start date plus the scheduling interval have elapsed. So, if our start date is setted to 2023/01/01 00:00 and we setted a daily interval, our DAG is effectively triggered at 2023/01/02 00:00 (one day elapsed) and then it will process all data from the start date.
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