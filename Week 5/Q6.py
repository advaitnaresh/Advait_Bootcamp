import pandas as pd

def replace_employee_id(employees: pd.DataFrame, employee_uni: pd.DataFrame) -> pd.DataFrame:
    # Merge using a left join to keep all employees even if they don't have a unique_id
    result = pd.merge(employees, employee_uni, on='id', how='left')
    
    # Return the specific columns in the requested order
    return result[['unique_id', 'name']]