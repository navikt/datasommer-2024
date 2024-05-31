from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from dataverk_airflow import python_operator, quarto_operator

dag_name = "eksempel_dag"
default_args = {
    "owner": "sommerteam",
    "start_date": datetime(2024, 5, 31),
    "depends_on_past": False,
    "retries": 1,
}
# Variable.get("SLACK_OPS_CHANNEL") er variabler satt i Airflow UI
slack_channel = Variable.get("SLACK_OPS_CHANNEL")
allowlist = Variable.get("STANDARD_ALLOWLIST").split(",")
env = Variable.get("ENVIRONMENT")

with DAG(
    dag_name,
    doc_md="Beskrivelse",
    default_args=default_args,
    schedule_interval="0 4 * * *", # daglig 04:00
    max_active_runs=1,
    catchup=False,
) as dag:
    task1 = python_operator(
        dag=dag,
        name="task1",
        repo="navikt/datasommer-2024",
        script_path="noe.py",
        slack_channel=slack_channel,
        allowlist=allowlist,
        extra_envs={"env": env},
        requirements="path_to_requirements_in_repo.txt",
    )
