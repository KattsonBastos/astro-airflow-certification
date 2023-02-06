# The Basics

[back to dag authoring page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In this section we'll learn how to define DAGs, their schedule interval and backfilling.
</p>

<p id="contents"></p>

## Contents
- <a href="#key">Key Notes about DAG files</a>
- <a href="#way">The Right Way of Defining DAGs</a>

---
<p id="key"></p>
  
## Key Notes about DAG files

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;An important thing to know, before we get started, is that the Airflow's Scheduler will only parse a .py file (inside our DAGs folder) to check whether it is a DAG or not only if it contains the word 'dag' or 'airflow' inside. Otherwise, Airflow won't generate our DAGs dinamically. Thus, just by importing the DAG class in our .py file the Scheduler will understand it is a DAG.
<br>

&ensp;&ensp;&ensp;&ensp;To modify this behavior, we have to set the 'DAG_DISCOVERY_SAFE_MODE' to false in Airflow's configuration. In this way, it'll try to parse all files.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Another important thing to keep in mind is if we have other Python files or other folders in the DAGs folder, we can add a '.airflowignore' in order to avoid Scheduler from trying to parse them. In that file, we can pass any file, folder or extension we don't want to parse.
</p>

---
<p id="way"></p>
  
## The Right Way of Defining DAGs

[back to contents](#contents)
