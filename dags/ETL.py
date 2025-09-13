from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook 
import json
from datetime import datetime, timedelta


## Define the DAG 
with DAG(
    dag_id = 'elt_pipeline',
    start_date = datetime.now() - timedelta(days=1),
    schedule = '@daily' 
) as dag :
    
    ## step 1 if it does not exist 
    @task
    def create_table():
        ##initialize postgress hook 
        hook = PostgresHook(postgres_conn_id="my_postgress_connection")

        #SQL querry to create a table 
        create_table_querry = """
    CREATE TABLE IF NOT EXISTS apod_data(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    explaination text,
    url TEXT,
    date DATE,
    media_type VARCHAR(50)
    );

    """
        # Execute the table creation query 
        hook.run(create_table_querry)





    ## step 2 Extract thhe NASA API Data(APOD)- Astronomy picture of the day [Extract Pipeline]
    ## https://api.nasa.gov/planetary/apod?api_key=ajhlV7ykEQ5hJBXQUYNcDhfShcuKF1lzLiFaaogB
    

    extract_apod=HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',  ## Connection ID Defined In Airflow For NASA API
        endpoint='planetary/apod', ## NASA API enpoint for APOD
        method='GET',
        data={"api_key":'{{conn.nasa_api.extra_dejson.api_key}}'}, ## USe the API Key from the connection
        response_filter=lambda response:response.json(), ## Convert response to json
    )




    ## step 3 Transform the data (Pick the information that i neeed to save )
    @task
    def transform_apod_data(response):
        apod_data = {
            'title' : response.get('title',''),# it means that if this is not present we are gonna get ''
            'explaination'  : response.get('explaination',''),
            'url' : response.get('url',''),
            'date' : response.get('date',''),
            'media_type':response.get('media_type','') 
        }
        return apod_data

    
    
    ## step 4 Load the data to the Postgress SQL
    @task
    def data_to_postgrees(apod_data):
        ## initialize the postgres Hook
        postgres_hook = PostgresHook(postgres_conn_id="my_postgress_connection")
        SQL_insert_query= """
        INSERT INTO apod_data (title,explaination,url,date,media_type)
        VALUES(%s,%s,%s,%s,%s);
        """
        ## Execute the SQl query 
        postgres_hook.run(SQL_insert_query, parameters=(
            apod_data['title'],
            apod_data['explaination'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))


    ## step 5 verify the data DBViewer
    ## step 6 Define the task dependencies 
    create_table_task = create_table()
    create_table_task >> extract_apod ## ensure table is created before extraction
    api_response  = extract_apod.output
    transformed_data  = transform_apod_data(api_response)
    data_to_postgrees(transformed_data)