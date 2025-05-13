
import pandas as pd
import pyodbc
from sqlalchemy import create_engine

def DataLoadCSV():
    Books = pd.DataFrame(pd.read_csv("Data/Raw/Books.csv")).dropna()
    Customers = pd.DataFrame(pd.read_csv("Data/Raw/Customers.csv")).dropna()

def DataDropNaDupe():
    Books = Books.dropna().dropduplicates()
    Customers = Customers.dropna().dropduplicates()


def DataCleaner():
    Books["Id"] = Books["Id"].astype(int)
    Books["Customer ID"] = Books["Customer ID"].astype(int)
    Customers["Customer ID"] = Customers["Customer ID"].astype(int)
    
    Books["Book checkout"] = Books["Book checkout"].replace("\"","",regex=True)
    Books.iloc[16] = Books.iloc[16].replace("32/05/2023","31/05/2023")
    
    Books["Book checkout"] = pd.to_datetime(Books["Book checkout"], format="mixed")
    Books["Book Returned"] = pd.to_datetime(Books["Book Returned"], format="mixed")

    Books["Books"] = Books["Books"].str.title()

def DataEnrich():
    Books["Days allowed to borrow"] = Books["Days allowed to borrow"].replace(" weeks","",regex=True).astype(int)
    Books["Days allowed to borrow"] = Books["Days allowed to borrow"]*7
    Books['Days on Loan'] = (Books['Book Returned'] - Books['Book checkout']).dt.days

def DataDumpSQL():
    connection_string = f'mssql+pyodbc://@localhost/LibraryDB?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    if __name__ == '__main__':
        try:
            Customers.to_sql('Customers', con=engine, if_exists='replace', index=False)
            Books.to_sql('Books', con=engine, if_exists='replace', index=False)
        except Exception as ex:
            print("Error: \n", ex)




DataLoadCSV
DataDropNaDupe
DataCleaner
DataEnrich
DataDumpSQL