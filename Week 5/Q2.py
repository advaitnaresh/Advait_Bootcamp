import pandas as pd

def fix_names(users: pd.DataFrame) -> pd.DataFrame:
    # Capitalize the first letter and lowercase the rest
    users['name'] = users['name'].str.capitalize()
    
    # Return sorted by user_id
    return users.sort_values(by='user_id')