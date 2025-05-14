import pandas as pd
import pyodbc
from sqlalchemy import create_engine

def DataLoadCSV(filepath):
    rawdata = pd.DataFrame(pd.read_csv(filepath))
    return rawdata
    
def DataDropNaDupe(df):
    df.dropna().drop_duplicates()
    return df

def DataCleaner(df, df2):

    df["Id"] = df["Id"].astype(int)
    df["Customer ID"] = df["Customer ID"].astype(int)
    df2["Customer ID"] = df2["Customer ID"].astype(int)
    
    df["Book checkout"] = df["Book checkout"].replace("\"","",regex=True)
    df.iloc[6] = df.iloc[6].replace("10/04/2063","10/04/2023")
    df.iloc[16] = df.iloc[16].replace("32/05/2023","31/05/2023")
    
    df["Book checkout"] = pd.to_datetime(df["Book checkout"], format="mixed")
    df["Book Returned"] = pd.to_datetime(df["Book Returned"], format="mixed")

    df["Books"] = df["Books"].str.title()

def DataEnrich(df):
    df["Days allowed to borrow"] = df["Days allowed to borrow"].replace(" weeks","",regex=True).astype(int)
    df["Days allowed to borrow"] = df["Days allowed to borrow"]*7
    df['Days on Loan'] = (df['Book Returned'] - df['Book checkout']).dt.days

def DataDumpSQL(df, df2):
    connection_string = f'mssql+pyodbc://@localhost/LibraryDB?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    if __name__ == '__main__':
        try:
            df.to_sql('Books', con=engine, if_exists='replace', index=False)
            df2.to_sql('Customers', con=engine, if_exists='replace', index=False)

        except Exception as ex:
            print("Error: \n", ex)

def DataOutCSV(df, df2):
    df.to_csv("Data/Processed/Books.csv", header=True)
    df2.to_csv("Data/Processed/Customers.csv", header=True)
    

def main():
    df = DataLoadCSV(filepath="Data/Raw/Books.csv")
    df2 = DataLoadCSV(filepath ="Data/Raw/Customers.csv")
    df = DataDropNaDupe(df)
    df2 = DataDropNaDupe(df2)
#    print(df.dropna())
#    DataCleaner(df, df2)
#    DataEnrich(df)
#    DataDumpSQL(df, df2)
    return df


if __name__ == '__main__':
    main()

