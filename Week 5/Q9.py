import pandas as pd

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    # Merge Employee and Department tables
    # We use suffixes because both tables have 'id' and 'name' columns
    merged = pd.merge(employee, department, left_on='departmentId', right_on='id', suffixes=('_emp', '_dept'))
    
    # Create a rank column based on salary within each department
    # method='dense' ensures tied values get the same rank, and the next rank is consecutive (1, 1, 2)
    merged['rank'] = merged.groupby('id_dept')['salary'].rank(method='dense', ascending=False)
    
    # Filter for rank <= 3
    top_earners = merged[merged['rank'] <= 3]
    
    # Rename columns to match the required output format
    result = top_earners.rename(columns={
        'name_dept': 'Department',
        'name_emp': 'Employee', 
        'salary': 'Salary'
    })
    
    # Return only the specific columns
    return result[['Department', 'Employee', 'Salary']]