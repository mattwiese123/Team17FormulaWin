from sqlalchemy import create_engine
import pandas as pd
import os


def get_data(query):
    PGHOST = os.getenv("PGHOST")
    PGPORT = os.getenv("PGPORT")
    PGUSER = os.getenv("PGUSER")
    PGPASSWORD = os.getenv("PGPASSWORD")
    PGDBNAME = os.getenv("PGDBNAME")
    engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(
            PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDBNAME
        )
    )
    df = pd.read_sql_query(query, engine)
    return df
