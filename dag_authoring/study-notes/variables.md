# Mastering Variables

[back to dag authoring page](https://github.com/KattsonBastos/astro-airflow-certification/tree/main/fundamentals)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Let's suppose we have multiple pipelines that use, let's say, the same GCS bucket. Should we put the bucket name inside all of our DAGs? That would be a such bad idea, since if for some reason we need to change the bucket path, we should edit DAG by DAG. So, what's the solution for this problem? That's where Airlfow's Variables comes in. In this section we'll talk a little bit about them.
</p>

<a name="readme-top"></a>

<p id="contents"></p>

## Contents
- <a href="#variables">Variables</a>
- <a href="#envs">Environment Variables</a>

---
<p id="variables"></p>
  
## Variables

[back to contents](#contents)

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Variables are basically an object of key-value pair stored in the metadata database. So, we can store variables such as an API endpoint, a bucket name, and so on, in a manner that when changed, they're are automatically applied to the entire Airflow instance. That brings us a lot of flexibility when dealing with that repeated information.
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
<p id="envs"></p>
  
## Environment Variables

[back to contents](#contents)


<p align="justify">
&ensp;&ensp;&ensp;&ensp;
</p>
