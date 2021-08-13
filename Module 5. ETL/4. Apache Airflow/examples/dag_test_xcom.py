from airflow.models import DAG
from datetime import datetime
from datetime import timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'Ivan',
    'depends_on_past': False,
    'email': ['ivan@theaicore.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2020, 1, 1), # If you set a datetime previous to the curernt date, it will try to backfill
    'retry_delay': timedelta(minutes=5),
    'end_date': datetime(2022, 1, 1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'trigger_rule': 'all_success'
}

with DAG(dag_id='test_dag_xcom',
         default_args=default_args,
         schedule_interval='*/1 * * * *',
         catchup=False,
         tags=['test']
         ) as dag:
    # Define the tasks. Here we are going to define only one bash operator
    t1 = BashOperator(task_id="t1",
                      bash_command='echo ~/Desktop',
                      do_xcom_push=True,
                      dag=dag,
                      )
    t2 = BashOperator(task_id="t2",
                      bash_command='pwd',
                      dag=dag,
                      )
    t3 = BashOperator(task_id="t3",
                      bash_command='echo "{{ti.xcom_pull(task_ids="t1")}}"',
                      dag=dag,
                      )

    t1 >> t2 >> t3