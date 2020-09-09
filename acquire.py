import os
import pandas as pd

#defines function to create a sql url using personal credentials
def get_db_url(db_name):
    
    #importing variables used to connect to sql database
    from env import host, username, password
    
    #creates the url and the function returns it
    url = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    return (url)

def get_titanic_data():

    if os.path.isfile('titanic_df.csv') == False:
        df = pd.read_sql('SELECT * FROM passengers', get_db_url('titanic_db'))
        df.to_csv('titanic_df.csv')
    else:
        df = pd.read_csv('titanic_df.csv', index_col=0)
    return df

def get_iris_data():

    if os.path.isfile('iris_df.csv') == False:
        sql_query = """
                    SELECT species_id,
                    species_name,
                    sepal_length,
                    sepal_width,
                    petal_length,
                    petal_width
                    FROM measurements
                    JOIN species
                    USING(species_id)
                    """
        df = pd.read_sql(sql_querry,get_db_url('iris_db'))
        df.to_csv('iris_df.csv')
    else:
        df = pd.read_csv('iris_df.csv', index_col=0)
    return df

