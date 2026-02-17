from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="simple_docker_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["docker", "hands-on"],
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command="echo '🚀 Airflow running in Docker'",
    )

    wait = BashOperator(
        task_id="wait",
        bash_command="sleep 5",
    )

    end = BashOperator(
        task_id="end",
        bash_command="echo '✅ DAG completed successfully'",
    )

    start >> wait >> end
