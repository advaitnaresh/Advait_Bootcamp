import pandas as pd

def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    # Group by pair and count occurrences
    grouped = actor_director.groupby(['actor_id', 'director_id']).count().reset_index()
    
    # Filter for counts >= 3 and return specific columns
    return grouped[grouped['timestamp'] >= 3][['actor_id', 'director_id']]
