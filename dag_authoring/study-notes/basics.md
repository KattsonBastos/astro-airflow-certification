# The Basics

[back to fundamentals page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this section we'll learn how to define DAGs, their schedule interval and backfilling.
</p>

<p id="contents"></p>

## Contents
- <a href="#way">The Right Way of Defining DAGs</a>

---
<p id="way"></p>
  
## The Right Way of Defining DAGs

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;An important thing to know, before we get started, is that the Airflow's Scheduler will only parse a .py file (inside our DAGs folder) to check if it is a DAG only if the it contains the word'dag' or 'airflow' inside. Otherwise, Airflow won't generate our DAGs dinamically. Thus, just by importing the DAG class in our .py file the Scheduler will understand it is a DAG.
<br>

To modify this behavior, we have to set the 'DAG_DISCOVERY_SAFE_MODE' to false in Airflow's configuration. In this way, it'll try to parse all files.
</p>