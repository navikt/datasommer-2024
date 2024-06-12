import pendulum
from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from dataverk_airflow import python_operator, quarto_operator

# 1. Hva er Airflow og hvor finnes det? Logge inn på teamet
# 2. Directed acyclic graph (DAG) samler tasks, som er filer som kjører kode
# 3. Hvordan kjøre en DAG og lese loggene
# 4. Variabler i Airflow UI, med feil og varsler
# 5. dataverk_airflow på PyPi fra Nada. Dokumentasjon tre steder
# 6. Argumenter til en DAG og til tasks
# 7. Task som henter BQ-data og oppdaterer en datafortelling

dag_name = "eksempel_dag"
default_args = {
    "owner": "sommertestteam",
    "depends_on_past": False,
}

# Variable.get("slack_ops_channel") er variabler satt i Airflow UI
# slack_channel = Variable.get("slack_channel")
# allowlist = Variable.get("allowlist").split(",")  # whitelist av domener
# env = Variable.get("env")

with DAG(
    dag_name,
    doc_md="Beskrivelse som kommer i Airflow UI",
    schedule_interval="0 6 * * *", # kronjob - daglig 06:00
    max_active_runs=1,
    start_date=datetime(2024, 5, 31, tzinfo=pendulum.timezone("Europe/Oslo")),
    catchup=False,
    default_args=default_args,
) as dag:
    task1 = python_operator(
        dag=dag,
        name="task1",
        repo="navikt/datasommer-2024",
        script_path="dags/dag_task1.py",
        # slack_channel=slack_channel,
        # allowlist=allowlist,
        # extra_envs={"env": env},
        # requirements="path_to_requirements_in_repo.txt",
    )
    # task2 = quarto_operator(
    #     dag=dag,
    #     name="lage_quarto",
    #     allowlist=allowlist,
    #     retries=0,
    #     repo="navikt/datasommer-2024",
    #     quarto={
    #         "path": "quarto/datafortelling.qmd",
    #         "format": "dashboard",
    #         "env": "prod",
    #         "id": "...",  # id fra URL på datamarkedsplassen
    #         "token": Variable.get("quarto_token"),
    #     },
    #     extra_envs={"env": env},
    #     slack_channel=slack_channel,
    #     requirements_path="./quarto/requirements.txt",
    # )
