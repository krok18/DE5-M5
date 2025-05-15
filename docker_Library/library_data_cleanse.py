import pandas as pd
# import pyodbc
# from sqlalchemy import create_engine

# Function to output dataframe that can be manipulated via a filepath
def fileLoader(filepath):
    data = pd.read_csv(filepath)
    return data 

# Duplicate Dropping Function
def duplicateCleaner(df):
    return df.drop_duplicates().reset_index(drop=True)

# NA handler - future scope can handle errors more elegantly. 
def naCleaner(df):
    return df.dropna().reset_index(drop=True)

# Turning date columns into datetime
def dateCleaner(col, df):

    # Strip any quotes from dates
    df[col] = df[col].str.replace('"', "", regex=True)

    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

    except Exception as e:
        print(f"Error while converting column {col} to datetime: {e}")

    # Identify rows with invalid dates
    error_flag = pd.to_datetime(df[col], dayfirst=True, errors='coerce').isna()
    
    # Keep only valid rows in df
    df = df[~error_flag].copy()

    # Reset index for the cleaned DataFrame
    df.reset_index(drop=True, inplace=True)

    return df

def enrich_dateDuration(colA, colB, df):
    """
    Takes the two datetime input column names and the dataframe to create a new column date_delta which is the difference, in days, between colA and colB.
    
    Note:
    colB>colA
    """

    df['date_delta'] = (df[colB]-df[colA]).dt.days

    #Conditional Filtering to be able to gauge eroneous loans.
    df.loc[df['date_delta'] < 0, 'valid_loan_flag'] = False
    df.loc[df['date_delta'] >= 0, 'valid_loan_flag'] = True

    #Conditional Filtering to be able to gauge late returns on loans.
    df.loc[df['date_delta'] > 14, 'returned_on_time'] = False
    df.loc[df['date_delta'] <= 14, 'returned_on_time'] = True
    df.loc[df['valid_loan_flag'] == False, 'returned_on_time'] = ""

    return df

"""
def writeToSQL(df, table_name, server, database):

    # Create the connection string with Windows Authentication
    connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    try:
        # Write the DataFrame to SQL Server
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)

        print(f"Table{table_name} written to SQL")
    except Exception as e:
        print(f"Error writing to the SQL Server: {e}")
"""
        
def writeToCSV(df, filepath):
    df.to_csv(filepath, header=True)



if __name__ == '__main__':
    print('**************** Starting Clean ****************')

    # Instantiation
    dropCount= 0
    customer_drop_count = 0
    filepath_input = './data/raw/Books.csv'
    date_columns = ['Book checkout', 'Book Returned']


    data = fileLoader(filepath=filepath_input)
    total_raw_books = len(data)

    # Drop duplicates & NAs
    data = naCleaner(data)

    total_na_removed_books = (total_raw_books - len(data))

    total_rolling_books = len(data) 

    data = duplicateCleaner(data)

    total_dupes_removed_books = (total_rolling_books - len(data))

    total_rolling_books = len(data)     

    # Converting date columns into datetime
    for col in date_columns:
        data = dateCleaner(col, data)

    total_errors_removed_books = (total_rolling_books - len(data))
    
    # Enriching the dataset
    data = enrich_dateDuration(df=data, colA='Book checkout', colB='Book Returned')

    #data.to_csv('cleaned_file.csv')
    print(data)

    total_clean_books = len(data)

    #Cleaning the customer file
    filepath_input_2 = './data/Raw/Customers.csv'

    data2 = fileLoader(filepath=filepath_input_2)

    total_raw_customers = len(data2)   

    # Drop duplicates & NAs

    data2 = naCleaner(data2)

    total_na_removed_customers = (total_raw_customers - len(data2))    

    total_rolling_customers = len(data2)

    data2 = duplicateCleaner(data2)

    total_dupes_removed_customers = (total_rolling_customers - len(data2))   

    print(data2)

    total_clean_customers = len(data2)

    print('**************** DATA CLEANED ****************')

    totals = pd.DataFrame({'total_raw_books': [total_raw_books],
                           'total_na_removed_books': [total_na_removed_books],
                           'total_dupes_removed_books': [total_dupes_removed_books],
                           'total_errors_removed_books': [total_errors_removed_books],
                           'total_raw_customers': [total_raw_customers],
                           'total_na_removed_customers': [total_na_removed_customers],
                           'total_dupes_removed_customers': [total_dupes_removed_customers],
                           'total_clean_books': [total_clean_books],
                           'total_clean_customers': [total_clean_customers]
                           })

    print(totals)

    print('Writing to CSV file...')

    filepath_output_1 = './data/Processed/Books.csv'
    filepath_output_2 = './data/Processed/Customers.csv'
    filepath_output_3 = './data/Processed/Totals.csv'    

    writeToCSV(
        data,
        filepath=filepath_output_1
    )

    writeToCSV(
        data2,
        filepath=filepath_output_2
    )

    writeToCSV(
        totals,
        filepath=filepath_output_3
    )

#    print('Writing to SQL Server...')

#    writeToSQL(
#        data, 
#        table_name='loans_bronze', 
#        server = 'localhost', 
#        database = 'DE5_Module5' 
#    )

#    writeToSQL(
#        data2, 
#        table_name='customer_bronze', 
#        server = 'localhost', 
#        database = 'DE5_Module5'
#    )

    print('**************** End ****************')