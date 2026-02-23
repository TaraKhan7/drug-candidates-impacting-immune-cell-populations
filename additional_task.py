# Additional Task: Determine the average number of B cells for responders at time=0 in melanoma males.

import sqlite3
import pandas as pd

connection = sqlite3.connect("cell-count.db")
join = pd.read_sql(
    """
    SELECT s.sex, s.condition, t. response, m.b_cell, m.time_from_treatment_start
    FROM Subjects AS s
    JOIN Treatments AS t ON s.subject_id = t.subject_id
    JOIN Samples as m ON m.subject_id = s.subject_id
    WHERE s.condition = 'melanoma' AND s.sex = 'M' AND t.response = 'yes' AND m.time_from_treatment_start = 0
    """,
    connection,
    )
print(join)

average = join['b_cell'].mean()
#print(average)
rounded = round(average, 2)
print('For Melanoma males, the average number of B cells for responders at time=0 is:', rounded)
