import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    # Get unique salaries sorted in descending order
    unique_salaries = employee['salary'].drop_duplicates().sort_values(ascending=False)
    
    # If fewer than 2 unique salaries exist, return None
    if len(unique_salaries) < 2:
        return pd.DataFrame({'SecondHighestSalary': [None]})
    
    # Return the second highest salary (index 1)
    return pd.DataFrame({'SecondHighestSalary': [unique_salaries.iloc[1]]})