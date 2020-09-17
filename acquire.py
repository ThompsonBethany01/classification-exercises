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

    # if file note already saved in csv, will create the df to csv
    if os.path.isfile('titanic_df.csv') == False:
        df = pd.read_sql('SELECT * FROM passengers', get_db_url('titanic_db'))
        df.to_csv('titanic_df.csv')

    #if already saved to csv file in computer
    else:
        df = pd.read_csv('titanic_df.csv', index_col=0)
    return df

def prep_titanic(titanic_df):
    # drop missing observations of embark town
    titanic_df = titanic_df[~titanic_df.embark_town.isnull()]

    #drop missing observations of embarked
    titanic_df = titanic_df[~titanic_df.embarked.isnull()]
    
    #remove deck column
    titanic_df = titanic_df.drop('deck',axis=1)
    
    #create dummy variables for embarked column
    df_dummies = pd.get_dummies(titanic_df['embarked'],drop_first=1)
    
    #add dummy variables to original df
    titanic_df = pd.concat([titanic_df, df_dummies], axis=1)
    
    #filling missing values in age with average age
    mode_age = titanic_df.age.mode().iloc[0]
    titanic_df['age'] = titanic_df.age.fillna(mode_age)
    
    return titanic_df

def get_iris_data():

    #if iris df not already saved to csv file
    if os.path.isfile('iris_df.csv') == False:

        # the sql querry which chooses the data uploaded to csv/df
        sql_query = """
                    SELECT species_id,
                    measurement_id,
                    species_name,
                    sepal_length,
                    sepal_width,
                    petal_length,
                    petal_width
                    FROM measurements
                    JOIN species
                    USING(species_id)
                    """
        #saves to df then csv
        df = pd.read_sql(sql_query,get_db_url('iris_db'))
        df.to_csv('iris_df.csv')
    
    #if already saved to csv in computer
    else:
        df = pd.read_csv('iris_df.csv', index_col=0)
    return df

def prep_iris(iris_df):
    #removing soecies_id column
    iris_df = iris_df.drop('species_id',axis=1)
    
    #dropping measurement_id column
    iris_df = iris_df.drop('measurement_id',axis=1)
    
    #renaming species column
    iris_df = iris_df.rename({'species_name':'species'},axis=1)
    
    #creating dummy variables for species names and add to df
    df_dummies = pd.get_dummies(iris_df['species'], drop_first=True)
    iris_df = pd.concat([iris_df, df_dummies], axis=1)
    
    return iris_df