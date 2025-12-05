import pandas as pd

def project_employees_i(project: pd.DataFrame, employee: pd.DataFrame) -> pd.DataFrame:
    # Merge project table with employee table to link experience years
    merged = pd.merge(project, employee, on='employee_id')
    
    # Group by project_id and calculate the mean experience
    result = merged.groupby('project_id')['experience_years'].mean().round(2).reset_index()
    
    # Rename column to match required output
    return result.rename(columns={'experience_years': 'average_years'})