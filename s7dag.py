from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
import pendulum
import requests
default_args = {
'owner': 'AGanshin',
'depends_on_past': False,
'start_date': pendulum.datetime(year=2022, month=6, day=1).in_timezone('Europe/Moscow'),
'email': ['alex@alex.ru'],
'email_on_failure': False,
'email_on_retry': False,
'retries': 0,
'retry_delay': timedelta(minutes=5)
}
#DAG1
dag1 = DAG('AGanshin001',
default_args=default_args,
description="seminar_7",
catchup=False,
schedule_interval='0 6 * * *')
task1 = BashOperator(
task_id='pyspark',
bash_command='export SPARK_HOME=/home/spark && export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin && python3 /home/airflow/dags/s6.py',
dag=dag1)
task2 = BashOperator(
task_id='spark',
bash_command='export SPARK_HOME=/home/spark && export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin && spark-shell -i /home/airflow/dags/s6s1.scala',
dag=dag1)
task2 >> task1
#DAG3
from airflow.operators.python import PythonOperator
import pandas as pd
from sqlalchemy import inspect,create_engine
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pandas.io import sql
import time
#pip install openpyxl
dag3 = DAG('AGanshin003',
default_args=default_args,
description="seminar_6",
catchup=False,
schedule_interval='0 8 * * *')
def hello(**kwargs):
  encoding="ISO-8859-1"
  print('Hello from {kw}'.format(kw=kwargs['my_keyword']))
  df=5+5
  print(df)
  df=pd.read_excel('/home/airflow/dags/s4_2.xlsx')
  con=create_engine("mysql://root:1@localhost:33061/spark")
  print(df)
  df['долг'] = df['Платеж по основному долгу'].cumsum()
  df['проценты'] = df['Платеж по процентам'].cumsum()
  df.to_sql('credit',con,schema='spark',if_exists='replace',index=False)
t2 = PythonOperator(
task_id='python3',
dag=dag3,
python_callable=hello,
op_kwargs={'my_keyword': 'Airflow 1'}
)
dag11 = DAG( 'hello_world' , description= 'Hello World DAG' , 
          schedule_interval= '0 12 * * *' , 
          start_date=datetime( 2023 , 1 , 1
          ), catchup= False ) 

hello_operator = BashOperator(task_id= 'hello_task' , bash_command='echo Hello from Airflow', dag=dag11)
hello_file_operator = BashOperator(task_id= 'hello_file_task' , bash_command='sh /home/airflow/dags/s6.sh ', dag=dag11) 
skipp_operator = BashOperator(task_id= 'skip_task' , bash_command='exit 99', dag=dag11) 

hello_operator >> hello_file_operator >> skipp_operator

def print_hello():
  return "hello, my little world"
def skip():
  return 99
  
dag22 = DAG( 'hello_world_22' , description= 'Hello_World_DAG' , 
          schedule_interval= '0 12 * * *' , 
          start_date=datetime( 2023 , 1 , 1
          ), catchup= False ) 
hello_operator2 = PythonOperator(task_id= 'hello_task2' , python_callable=print_hello, dag=dag22)
skipp_operator2 = PythonOperator(task_id= 'skip_task2' , python_callable=skip, dag=dag22)
hello_file_operator2 = BashOperator(task_id= 'hello_file_task2' , bash_command='sh /home/airflow/dags/s6.sh ', dag=dag22)
  

hello_operator2 >> hello_file_operator2 >> skipp_operator2


def hw_7_get_temp(**kwargs) :

  ti = kwargs ['ti']
  
  city = "Lipetsk"
  
  api_key = "9e09ab59b55473a15edd2c94a4dba25c"
  
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city} & appid={api_key}"
  
  payload = {}
  
  headers = {}
  
  response = requests. request ("GET", url, headers=headers, data=payload)
  
  # ti.xcom_push(key='hw_7_open_weather', value=round (float (response. json() ['main'] ['temp']) -273.15, 2)
  
  return round(float (response.json() ['main']['temp']) -273.15, 2)

def hw_7_check_temp(ti):

  temp = int(ti.xcom_pull(task_ids='hw_7_get_temperature_task') )
  
  print(f' Temperature now is {temp}')
  
  if temp >= 15:
  
    return 'hw_7_print_warm' 
    
  else:
  
    return 'hw_7_print_cold'

with DAG(

  'hw_7_wather_chek_warm_or_cold',
  
  start_date=datetime(2024, 1, 1),
  
  catchup=False,
  
  tags=['homework_ETL'],

) as dag:

  hw_7_get_temperature_task = PythonOperator(
  
  task_id='hw_7_get_temperature_task',
  
  python_callable=hw_7_get_temp,

)

  hw_7_check_temperature_task = BranchPythonOperator(
  
  task_id='hw_7_check_temperature_task',
  
  python_callable=hw_7_check_temp,

)

  hw_7_print_warm = BashOperator(
  
  task_id='hw_7_print_warm',
  
  bash_command='echo "It is warm"',

)

  hw_7_print_cold = BashOperator(
  
  task_id='hw_7_print_cold',
  
  bash_command='echo "It is cold"',

)

hw_7_get_temperature_task >> hw_7_check_temperature_task >> [
    hw_7_print_warm, hw_7_print_cold]
