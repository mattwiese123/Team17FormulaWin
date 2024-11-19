from sqlalchemy import create_engine
import pandas as pd

def get_data(query):
    host= "capstone-database.cxy4yu8cqqaj.us-east-1.rds.amazonaws.com"
    port= "5432"
    user= "fwin_readonly"
    password= "Capstone_F1_8522"
    dbname= "postgres"
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname))
    df = pd.read_sql_query(query, engine)
    return df

