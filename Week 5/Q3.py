import pandas as pd

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    # Merge person table with address table using a left join
    merged = pd.merge(person, address, on='personId', how='left')
    
    # Return specific columns
    return merged[['firstName', 'lastName', 'city', 'state']]