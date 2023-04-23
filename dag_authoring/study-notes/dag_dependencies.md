# Dag Dependencies

[back to dag authoring page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)


<a name="readme-top"></a>

<p id="contents"></p>

## Contents
- <a href="#sensor">ExternalTaskSensor: waiting for multiple DAGs</a>
- <a href="#operator">TriggerDagRunOperator</a>

---
<p id="sensor"></p>
  
## ExternalTaskSensor: waiting for multiple DAGs

<p align="justify">
&ensp;&ensp;&ensp;&ensp;ExternalTaskSensor will wait for a task in another DAG to complete before it moves forward. The implementation is very simple:
</p>


```python
waiting_for_task = ExternalTaskSensor(
    task_id="waiting_for_task",
    external_dag_id="my_dag",
    external_task_id="task_one"
)

```

<p align="justify">
&ensp;&ensp;&ensp;&ensp;By specifying the external dag id and the desired task,it will wait for the completion of that task. It is important to remember that the sensor waits for the current executon date. If the external task takes longer than this time, the sensor will never succeed (and timeout after 7 days, by default).
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
<p id="operator"></p>
  
## TriggerDagRunOperator

<p align="justify">
&ensp;&ensp;&ensp;&ensp;This operator allows us to trigger another DAG. Follows a use example:
</p>

```python
waiting_for_task = TriggerDagRunOperator(
    task_id="triggering",
    trigger_dag_id="target_dag",
    execution_date='{{ ds }}',  # str or datetime
    wait_for_completion=False,
    poke_interval=60,
    reset_dag_run=True,
    failed_states=['failed']
)

```

- trigger_dag_id: the id of the DAG we want to trigger
- execution_date: execution date we want to start the target DAG -> useful for backfilling
- wait_for_completion: defines whether or not to wait for the target DAG completion before moving to the next task.
- poke_interval: frequency it will check if the DagRun completed.
- reset_dag_run: reset DagRun execution. useful in case of failure, that is, if the triggered DagRun fails, the only way to execute it again is by cleaning. This parameters helps with this.
- failed_states: what states the task could expect to consider that the triggered DagRun have failed.

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Even though it is similiar to a sensor, it is not.
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>