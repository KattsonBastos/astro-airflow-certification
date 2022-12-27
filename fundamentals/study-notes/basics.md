# The Basics

---
## Why to use Airflow and why to use it instead of Cron Jobs (or any other)?

<p align="justify">
&ensp;&ensp;&ensp;&ensp;To answer that questions, let's image we are working on an ETL pipeline, extracting data from an API, transforming them with Dbt, and, finally, loading them into a database. What would happen if the request to the API falied? Or if the database goes down? If we have just a few pipelines to manage, it becomes simple to manage those exception. Even so, having a easier way to rerun our pipeline would be very helpful.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The thing is many times we have to build a lot of different and independent data pipelines in which they require different components, dependencies, and data sources/destinations. So, the question is: without an orchestration tool, would we be able to handle all exceptions that could come in? Even if we would, is that worth the time? Most of the times the answer is 'no'.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;That's where Airflow comes in: it helps us with the orchestration of the workflow. However, we have many other options to use, such as Cron jobs, so, why to choose Airflow in the case of data pipelines? 
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Well, each tool has its advantages and disadvantages. In the case o Cron, it can't handle complex dependencies between tasks, it doesn't allow us to automatically monitor our tasks or to rerun our tasks after some failure.
</p>

---
## Airflow and its Benefits

<p align="justify">
&ensp;&ensp;&ensp;&ensp;According to <a href="https://airflow.apache.org/docs/apache-airflow/stable/index.html">the documentation</a>, Airflow is a platform (and open-source) used for workflow's <strong>development, scheduling, and monitoring</strong>. In addition, it allows us to build workflows connected with many other technologies, such as container's orchestrators and cloud services.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;A more simple definition is that Airflow is an "orchestrator for creating and executing tasks in the right order, in the right way, and at the right time." (Marc Lamberti in Airflow Fundamentals lectures).
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;We have a lot of benefits when using Airflow in data pipelines. Some of them:
</p>

- Dynamic: Airflow is coded in python, so, anything we can do in Python, we can do in our data pipelines.

- Scalable: we can execute as many tasks as we want.

- Interactive: we have three ways to interact with airflow. The first one is the user interface that helps us monitor our Dags; the second is the CLI; the last, a Rest API that allows us to execute specific tasks.

- Extensible: we can customize it as much as we need. In this way, we can create our own pluging and add it to Airflow.

---
## What Airflow is not

<p align="justify">
&ensp;&ensp;&ensp;&ensp;It is important to say that Airflow is not a streaming or a data processing framework. Airflow can't be used as Spark for processing terabytes of data or to handle real-time data flow.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;So, what to do if we have terabytes of data to process? Simple: we just have to trigger a Spark job from Airflow and let it do all the job.
</p>

---
## Airflow Core Components

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Under the hood, Airflow runs a lot of components:
</p>

- Three core components: a Web Server, a Scheduler, and a Metadata Database.
- Two additional components: an Executor and Workers.

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The first one, the <strong>Web Server</strong>, is a Flask app with Gunicorn that serves the user interface that allows us to monitor our tasks.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The second component is the <strong>Scheduler</strong>. The Scheduler is the heart of Airflow. Without it, we won't be able to trigger our workflows.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The next one, the <strong>Metadata Database</strong>, is a component that stores all data related to users, jobs, varaibles, and connections (among many other). But what databases could we use as Airflow metadata storage? We could use any one that is compatible with Sqlalchemy, such as Postgres and MySql.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In order to define how our tasks are going be executed, Airflow has a <strong>Executor</strong> component. So, we have specific executors for running tasks on local machines or on a Kubernetes Cluster.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Finally, the <strong>Worker</strong> is a process/subprocess where our task is actually going to be executed.
</p>

## Architectures: components working together

<p align="justify">
&ensp;&ensp;&ensp;&ensp;There are thounsands of architectures we could use in Airflow, but let's start simple by taking a look at two types: one node and multi node archutectures.
</p>

### Single Node: the simplest architecture we can have

<img src="../images/one-node.jpg" alt="drawing" width="100%"/>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this architecture, all Airflow components run on the same machine. However, how they work together? It's simple:
</p>

1. First, the Web Server interacts with the Metadata Store. It fetches all the data it needs from the metastores: data from tasks, users, permissions, connections.
2. If a task is ready to be scheduled, the Scheduler changes it state in the Metastore, create an object of that task and sends it into the queue of the Executor.
3. The Executor interacts with the Metastore in order to update task's state once it's done.


<p align="justify">
&ensp;&ensp;&ensp;&ensp;Here we see the importance of the Metastore since all other components interact with it. Also, the Web Server interacts directly only with the Metastore.
</p>

### Multi Nodes: scaling up Airflow
<img src="../images/multi-node.jpg" alt="drawing" width="100%"/>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In a scenario where we want to execute as many tasks as we would want, a very simple architecture could not be able to handle it. Then, we would need to set up a new architecture and, more specifically, a multi node architecture.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this case, we could keep the components separatelly in different nodes, specially the workers, where the task is processed.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;So, we could keep the Web Server, the Scheduler and the Executor in one node, and the Metastore and the Queue in a second node, separating it from the Executor.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this case:
</p>

1. The Web Server still interacts with the Metasore..
2. The Scheduler interacts with the Metastore to change the task state. Once a task is ready to run, it creates an object of that task and sends it to the Executor.
3. The executor sends the task it received from the Scheduler to the Queue.
4. Once the task is in the Queue, it is ready to be pull and executed by one of the workers.

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The idea of having separate nodes for the workers is to gain the ability to scale down and up our processing capacity: if we need to execute more tasks, we can raise up more nodes to process them.
</p>

## Core concepts we need to know

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In order to fully understand Airflow, we have to know some important concepts.
</p>

### DAG - Directed Acyclic Graph

<img src="../images/simple-dag.jpg" alt="drawing" width="100%"/>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In Airflow, when we create a data pipeline, we are actually creating a DAG. A DAG is simply a collection of all tasks (the workflow) defined as a graph. The dependency between the tasks must be acyclic, not cyclic (it is not possible ot have loops in our DAGs). In the image above, for example, the data transformation is only executed when both data extraction are done.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;
The idea of a DAG is to wrap up all of our tasks, the relationship between them, and their depencencies.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;
The idea of a DAG is to wrap up all of our tasks, the relationship between them, and their depencencies.
</p>

### Operators

<p align="justify">
&ensp;&ensp;&ensp;&ensp;An Operator is a task in our DAG: whenever we define a operator, we are creating a task in our DAG. In this way, they define what is going to be executed: a bash command, a python function, a SQL query, among many others. For each task we want to run in our pipeline, we instantiate an Operator.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;There are three types of Operators: <strong>Action</strong>, <strong>Transfer</strong> and <strong>Sensor</strong>:
</p>

- Action Operators: allows us to execute something, such as a python script, a bash command, or a SQL query.
- Transfer Operator: allows us to transfer data from a source to a destination.
- Sensor Operator: usefull when we want to wait for something to happen before moving to the next task. For example, if we want to wait for a file to be loaded in to a S3 storage to, then, download that file with a task, we could use a File Sensor Operator for that.

### Tasks
<p align="justify">
&ensp;&ensp;&ensp;&ensp;A Task is basically an instance of an Operator. Once it is ready to be scheduled, it becomes a Task Instance Object: it represents a specific run of a task -> DAG + Task + point in time.
</p>

### Dependencies
<p align="justify">
&ensp;&ensp;&ensp;&ensp;It is relationships between tasks. With dependencies, we can set upstream and downstream tasks dependencies.
</p>

### Workflow
<p align="justify">
&ensp;&ensp;&ensp;&ensp;A Workflow is the combination of all concepts we saw before.
</p>

## The lifecycle of a Task

<p align="justify">
&ensp;&ensp;&ensp;&ensp;(TODO)
</p>