# Part 3: Statistical Analysis
import sqlite3
import pandas as pd

connection = sqlite3.connect("cell-count.db")

# Query SQL

join = pd.read_sql(
    """
    SELECT s.subject, t. response, y.population, y.percentage
    FROM Subjects AS s
    JOIN Treatments AS t ON s.subject_id = t.subject_id
    JOIN Projects AS p ON p.project_id = s.project_id
    JOIN Samples as m ON m.subject_id = s.subject_id
    JOIN Summary as y ON y.sample_id = m.sample_id
    WHERE s.condition = 'melanoma' AND t.treatment = 'miraclib' AND p.sample_type = 'PBMC'
    """,
    connection,
)
#print(join)


df_yes = join[join["response"]=='yes']
df_no= join[join["response"]=='no']


import matplotlib.pyplot as plt
df_yes.boxplot(column="percentage", by="population", grid=False)
plt.title("Relative Frequency for 'Yes' Response ")
plt.suptitle("")  # Remove default title
plt.xlabel("Cell Population ")
plt.ylabel("Percentage")
plt.savefig("boxplot_yes.png", dpi=300)  

plt.clf() 
df_no.boxplot(column="percentage", by="population", grid=False)
plt.title("Relative Frequency for 'No' Response ")
plt.suptitle("")  # Remove default title
plt.xlabel("Cell Population ")
plt.ylabel("Percentage")
plt.savefig("boxplot_no.png", dpi=300) 