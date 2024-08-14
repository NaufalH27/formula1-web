import datetime
import logging
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
import fetchf1Data as fetchf1Data




default_args = {
    'owner': 'airflow',
    'retries' : 3,
    "retry_delay": datetime.timedelta(minutes=1),
}
dag = DAG(
     dag_id="fetch_testing",
     start_date=datetime.datetime(2024, 8, 11),
     schedule_interval='@daily'
 )





fetch_race_info_task = PythonOperator(
    task_id='fetch_race_info',
    python_callable=fetchf1Data.fetch_race_info,
    dag=dag,
)

fetch_race_result_task = PythonOperator(
    task_id='fetch_race_result',
    python_callable=fetchf1Data.fetch_race_result,
    dag=dag,
)

fetch_qualifying_data_task = PythonOperator(
    task_id='fetch_qualifying_data',
    python_callable=fetchf1Data.fetch_qualifying_data,
    dag=dag,
)

fetch_sprint_data_task = PythonOperator(
    task_id='fetch_sprint_data',
    python_callable=fetchf1Data.fetch_sprint_data,
    dag=dag,
)

ingesting = PythonOperator(
    task_id='ingest_all_data',
    python_callable=ingest,
    dag=dag,

)

[fetch_race_info_task , fetch_race_result_task, fetch_qualifying_data_task, fetch_sprint_data_task] >> ingesting