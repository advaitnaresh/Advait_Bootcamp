SELECT ROUND(COUNT(t2.player_id) / COUNT(t1.player_id), 2) AS fraction
FROM (
    -- Step 1: Find the first login date for each player
    SELECT player_id, MIN(event_date) AS first_login
    FROM Activity
    GROUP BY player_id
) t1
LEFT JOIN Activity t2 
    -- Step 2: Join to check if there is a record exactly 1 day after the first login
    ON t1.player_id = t2.player_id 
    AND t2.event_date = DATE_ADD(t1.first_login, INTERVAL 1 DAY);