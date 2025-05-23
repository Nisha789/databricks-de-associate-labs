# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab: Modular Orchestration
# MAGIC
# MAGIC In this lab, you'll be configuring a multi-task job comprising of three notebooks.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC By the end of this lab, you should be able to:
# MAGIC * Schedule a Master Job consists of SubJobs (RunJobs)

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - SELECT CLASSIC COMPUTE
# MAGIC
# MAGIC Before executing cells in this notebook, please select your classic compute cluster in the lab. Be aware that **Serverless** is enabled by default.
# MAGIC
# MAGIC Follow these steps to select the classic compute cluster:
# MAGIC
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select your cluster. By default, the notebook will use **Serverless**.
# MAGIC
# MAGIC 1. If your cluster is available, select it and continue to the next cell. If the cluster is not shown:
# MAGIC
# MAGIC   - In the drop-down, select **More**.
# MAGIC
# MAGIC   - In the **Attach to an existing compute resource** pop-up, select the first drop-down. You will see a unique cluster name in that drop-down. Please select that cluster.
# MAGIC
# MAGIC **NOTE:** If your cluster has terminated, you might need to restart it in order to select it. To do this:
# MAGIC
# MAGIC 1. Right-click on **Compute** in the left navigation pane and select *Open in new tab*.
# MAGIC
# MAGIC 1. Find the triangle icon to the right of your compute cluster name and click it.
# MAGIC
# MAGIC 1. Wait a few minutes for the cluster to start.
# MAGIC
# MAGIC 1. Once the cluster is running, complete the steps above to select your cluster.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this course. It will also set your default catalog to **dbacademy** and the schema to your specific schema name shown below using the `USE` statements.
# MAGIC <br></br>
# MAGIC ```
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA dbacademy.<your unique schema name>;
# MAGIC ```
# MAGIC
# MAGIC **NOTE:** The **DA** object is only used in Databricks Academy courses and is not available outside of these courses.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup-5L

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Create a Starter Job

# COMMAND ----------

# MAGIC %md
# MAGIC Run the cell below to use the custom `DA` object to create a starter job for this demonstration. After the cell completes, it will create a job named **\<your-schema>_Lesson_05** with three individual jobs.
# MAGIC
# MAGIC **NOTE:** The following custom method uses the Databricks SDK to programmatically create a job for demonstration purposes. You can find the method definition that uses the Databricks SDK to create the job in the [Classroom-Setup-Common]($./Includes/Classroom-Setup-Common) notebook. However, the [Databricks SDK](https://databricks-sdk-py.readthedocs.io/en/latest/) is outside the scope of this course.

# COMMAND ----------

DA.create_job_lesson05()

# COMMAND ----------

# MAGIC %md
# MAGIC ##C. Using the `Run Job` Task Type
# MAGIC We are going to configure a job that has three "sub-jobs" where each sub-job will be a Task. The bundle we just deployed configured these sub-jobs for us. 
# MAGIC
# MAGIC To confirm this, from fly-in menu, go to *Workflows* > *Jobs*.  You will see a **...Job1**, **...Job2** and **...Job3**.
# MAGIC
# MAGIC To setup the full job, complete the following:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Creating a Master Job and adding Run Job as a task
# MAGIC 1. Right-click on **Workflows** in the left navigation bar, and open the link in a new tab.
# MAGIC 2. Click **Create job**, and give it the name of **your-schema - Modular Orchestration Job**
# MAGIC 3. For the first task, complete the fields as follows:
# MAGIC
# MAGIC Configure the task:
# MAGIC
# MAGIC | Setting | Instructions |
# MAGIC |--|--|
# MAGIC | Task name | Enter **Ingest_From_Source_1** |
# MAGIC | Type | Choose **Run Job** |
# MAGIC | Job | Start typing "job_1". You should see a job that is named -> **[your-schema]_Lesson_5_job_1** Select this job.|
# MAGIC
# MAGIC 4. Click **Create task**
# MAGIC
# MAGIC ![Lesson05_RunJob1](files/images/deploy-workloads-with-databricks-workflows-2.0.2/Lesson05_RunJob1.png)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Add another Run Job as task
# MAGIC Now, configure the second task similar to first task. The second task is already a job being created as **[your_schema]_Lesson_5_Job_2**
# MAGIC 1. Complete the fields as follows:
# MAGIC Configure the task:
# MAGIC
# MAGIC | Setting | Instructions |
# MAGIC |--|--|
# MAGIC | Task name | Enter **Ingest_From_Source_2** |
# MAGIC | Type | Choose **Run Job** |
# MAGIC | Job | Start typing "job_2". You should see a job that is named -> "[your-schema]_Lesson_5_job_2" Select this job.|
# MAGIC |Depends on| Click the "x" to remove **Ingest_From_Source_1** from the list.
# MAGIC
# MAGIC <br>
# MAGIC
# MAGIC 2. Click **Create task**
# MAGIC
# MAGIC ![Lesson05_RunJob2](files/images/deploy-workloads-with-databricks-workflows-2.0.2/Lesson05_RunJob2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### C3. Adding a Dependent Run Job as task
# MAGIC In our scenario, we are configuring two tasks that run jobs that ingest data from two different sources (however, these example jobs do not actually ingest any data). We are now going to configure a third task that runs a different job that is designed to perform data cleaning:
# MAGIC 1. Complete the fields as follows:
# MAGIC Configure the task:
# MAGIC
# MAGIC | Setting | Instructions |
# MAGIC |--|--|
# MAGIC | Task name | Enter **Cleaning_Data** |
# MAGIC | Type | Choose **Run Job** |
# MAGIC | Job | Start typing "job_3". You should see a job that is named -> "[your-schema]_Lesson_5_job_3" Select this job.|
# MAGIC |Depends on| Click inside the field, and select **`Ingest_From_Source_2`**, and **`Ingest_From_Source_1`** to add it to the list
# MAGIC |Dependencies| Verify that "All succeeded" is selected.
# MAGIC
# MAGIC <br>
# MAGIC
# MAGIC 2. Click **`Create task`**
# MAGIC
# MAGIC
# MAGIC ![Lesson05_RunJob3](files/images/deploy-workloads-with-databricks-workflows-2.0.2/Lesson05_RunJob3.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ##D. Job Parameters
# MAGIC In a previous lesson, we configured "Task parameters" that passed key/value data to individual tasks. In the job we are currently configuring, we want to pass key/value data to *all* tasks. We can use "Job parameters" to perform this action.
# MAGIC
# MAGIC
# MAGIC
# MAGIC 1. On the right side of the job configuration page, find the section called **`Job parameters`**, and click **`Edit parameters`**.
# MAGIC 1. Add a parameter as follows:
# MAGIC   * Key: **test_value** --- Value: **Succeed**
# MAGIC 3. Click **`Save`**.
# MAGIC
# MAGIC ![Lesson05_MasterJob_1](files/images/deploy-workloads-with-databricks-workflows-2.0.2/Lesson05_MasterJob_1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ##E. Run the Job
# MAGIC Click **`Run now`** to run the job

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>