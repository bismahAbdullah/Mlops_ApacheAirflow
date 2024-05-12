from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import csv
import requests
from bs4 import BeautifulSoup

# Step 2: Define default arguments for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Step 3: Initialize the DAG object
dag = DAG(
    'mlops_assignment',
    default_args=default_args,
    description='DAG for MLOps assignment',
    schedule_interval=timedelta(days=1),
)

# Step 4: Define tasks
def scrape_bbc_links():
    url = "https://www.bbc.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")
        bbc_links = [link.get("href") for link in links if link.get("href")]
        bbc_links = [link for link in bbc_links if "http" in link]
        return bbc_links
    else:
        return []

def save_links_to_csv(**kwargs):
    ti = kwargs['ti']
    bbc_links = ti.xcom_pull(task_ids='scrape_bbc_links_task')
    with open("/path/to/bbc_links.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Links"])
        for link in bbc_links:
            writer.writerow([link])

# Step 5: Define operators
scrape_bbc_links_task = PythonOperator(
    task_id='scrape_bbc_links_task',
    python_callable=scrape_bbc_links,
    dag=dag,
)

save_links_to_csv_task = PythonOperator(
    task_id='save_links_to_csv_task',
    python_callable=save_links_to_csv,
    provide_context=True,
    dag=dag,
)

# Step 6: Configure task dependencies
scrape_bbc_links_task >> save_links_to_csv_task

# Step 7: Define DAG structure
