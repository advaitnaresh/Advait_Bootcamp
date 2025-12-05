import pandas as pd

def gameplay_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    # Ensure event_date is strictly datetime format
    activity['event_date'] = pd.to_datetime(activity['event_date'])
    
    # Step 1: Find the first login date for every player
    first_logins = activity.groupby('player_id')['event_date'].min().reset_index()
    
    # Step 2: Calculate the date immediately following the first login
    first_logins['next_day'] = first_logins['event_date'] + pd.Timedelta(days=1)
    
    # Step 3: Merge back with original data to find matches
    # We look for rows where player_id matches and the event_date matches our calculated 'next_day'
    matches = pd.merge(first_logins, activity, 
                       left_on=['player_id', 'next_day'], 
                       right_on=['player_id', 'event_date'])
    
    # Step 4: Calculate fraction
    # Numerator: Count of players who logged in the next day (len of matches)
    # Denominator: Total count of distinct players (len of first_logins)
    total_players = len(first_logins)
    
    if total_players == 0:
        return pd.DataFrame({'fraction': [0.0]})
        
    fraction = round(len(matches) / total_players, 2)
    
    return pd.DataFrame({'fraction': [fraction]})