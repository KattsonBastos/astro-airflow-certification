# Interacting with Apache Airflow

<p id="contents"></p>

## Contents 
- <a href="#3-ways">Three ways to interact with Airflow</a>
- <a href="#ui">Diving into the Airflow UI</a>
- <a href="#cli">Important CLI Commands to know</a>
- <a href="#rest">A little more about the Airflow REST API</a>

---
<p id="3-ways"></p>

## Three ways to interact with Airflow

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;There are three difference ways we can interact with Apache Airflow: User Interface, Command Line Interface, and a Rest API. So, let's take a brief look at them.
</p>

### User Interface (UI)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Airflow's UI allows us to manage and monitor our pipelines: checking logs, get the history of dag runs, and so on. The UI allows us to monitor our DAGs in many different ways: Graph View, Grid View, Calendar View, Code View. We'll take a better look at them later.
</p>

### Command Line Interface (CLI)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Most of the times we are going to use the UI for interaction. But there are some special cases when we need to use the CLI. According to <a href="https://airflow.apache.org/docs/apache-airflow/1.10.2/cli.html">the docs</a>, Airflow CLI allows many types of operations: to start some service; supporting developments; testing a DAG. Besides that, we also need the CLI when we need to update Airflow and to initialize Airflow.
</p>

### REST API

<p align="justify">
&ensp;&ensp;&ensp;&ensp;When we need to build something on top or Airflow, its REST API becomes very useful. Also, it allows us to trigger DAGs, pass arguments to them, and a lot more benefits
</p>

---
<p id="ui"></p>

## Diving into the Airflow UI

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Important: depending on your Airflow version, the following notes and images could be different from your UI. 
</p>

### DAG View

<img src="../images/dag-view.png" alt="drawing" width="100%"/>


<p align="justify">
&ensp;&ensp;&ensp;&ensp;Once we are logged in Airflow, the first view is the DAGs View. It lists all DAGs we have in our DAGs folder. Besides that, it brings a lot of information, such as the datetime of the last run, the schedule, allows us to trigger the DAG, and so on.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;The image above shows us a DAGs View with an example DAG - etl_pipeline. Inthat view, we have:
</p>

1. A toggle (to the left of the DAG's name): it defines whether of not the DAG is ready to be scheduled. It's important to keep it activated even if we only want to manually trigger the DAG.
2. The name of the DAG: the name that appears there is the name we wsetted shen creating it.
3. Owner: usually, we put unique names to the owner. It is useful to prevent users from running tasks from a specific owner.
4. Runs: it allows us to see the status of current and past runs. Respectivelly, those four circles shows the status:  queued, success, running, failed.
5. Scheduling interval: the time interval at which our DAG is triggered.
6. Last Run: execution date when our DAG was triggered for the last time (the beginning of the scheduling period).
7. Next Run: the expected date and time of the next run.
8. Recent Tasks Status: status for all active DAGs, or for the most recent runs.
9. Actions: allows us to manually trigger or to remove a DAG. The deletion does not delete the file that contains our DAG, it only delete the metadata related to our DAG.
10. Lastly, the Links: it allows us to have specific views and details of a DAG.

### Tree View and Grid View

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Tree View allows us to see the history of execution of the current DAG along with the status of each task
</p>

<img src="https://airflow.apache.org/docs/apache-airflow/2.2.0/_images/tree.png" alt="drawing" width="100%"/>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Here, the circles corresponds to the dag and the squares to the tasks. Once a DAG is started, we can follow its status progress in this view.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In version 2.3, this view was replaced by a Grid View, which can do more things and brings us a lot more information.
</p>

<img src="https://airflow.apache.org/docs/apache-airflow/2.3.0/_images/grid.png" alt="drawing" width="100%"/>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;On the left, we have somthing similar to the Tree, but now, for each task, we also have its duration. On the right, the display will change dependening on our interaction: by default, it shows the DAG details, such as the total of success and failures, first run, and etc.; if we click on some of that execution bar, it will display the execution details; and, if we click on a specific status box of a task instance, it will display the task details, such as the used Operator, last and next run.
</p>

### Graph View

<img src="../images/graph-view.png" alt="drawing" width="100%"/>

### Grantt View

<img src="../images/grantt-view.png" alt="drawing" width="100%"/>

---
<p id="cli"></p>

## Important CLI Commands to know

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp; (_TODO_)
</p>

---
<p id="rest"></p>

## A little more about the Airflow REST API

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp; (_TODO_)
</p>

