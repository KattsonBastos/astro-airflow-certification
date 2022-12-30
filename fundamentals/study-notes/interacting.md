# Interacting with Apache Airflow

<p id="contents"></p>

## Contents 
- <a href="#3-ways">Three ways to interact with Airflow</a>
- <a href="#ui">Diving into the Airflow UI</a>

---
<p id="3-ways"></p>

## Three ways to interact with Airflow

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

<p align="justify">
&ensp;&ensp;&ensp;&ensp;
</p>

