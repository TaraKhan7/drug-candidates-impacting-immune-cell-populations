# Part 2- Initial Analysis- Data Overview
import sqlite3
import pandas as pd

connection = sqlite3.connect("cell-count.db")

# Query SQL for samples table
df = pd.read_sql(
    "SELECT sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte FROM Samples;",
    connection,
)

# Calcuate totals for each row
df["total_count"] = (
    df["b_cell"] + df["cd8_t_cell"] + df["cd4_t_cell"] + df["nk_cell"] + df["monocyte"]
)

# Calculate percentage for each row
cell_type = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]

for column in cell_type:
    df[column + " percentage"] = (df[column] / df["total_count"]) * 100


df_new = pd.DataFrame(
    columns=["sample", "total_count", "population", "count", "percentage"]
)

# Format Results Table
for row in df.to_dict(orient="records"):
    new_rows_to_add = [
        {
            "sample": row["sample"],
            "total_count": row["total_count"],
            "population": "b_cell",
            "count": row["b_cell"],
            "percentage": row["b_cell percentage"],
        },
        {
            "sample": row["sample"],
            "total_count": row["total_count"],
            "population": "cd8_t_cell",
            "count": row["cd8_t_cell"],
            "percentage": row["cd8_t_cell percentage"],
        },
        {
            "sample": row["sample"],
            "total_count": row["total_count"],
            "population": "cd4_t_cell",
            "count": row["cd4_t_cell"],
            "percentage": row["cd4_t_cell percentage"],
        },
        {
            "sample": row["sample"],
            "total_count": row["total_count"],
            "population": "nk_cell",
            "count": row["nk_cell"],
            "percentage": row["nk_cell percentage"],
        },
        {
            "sample": row["sample"],
            "total_count": row["total_count"],
            "population": "monocyte",
            "count": row["monocyte"],
            "percentage": row["monocyte percentage"],
        },
    ]

    df_add = pd.DataFrame(new_rows_to_add)

    df_new = pd.concat([df_new, df_add], ignore_index=True)



# Display summary results table

# Uncomment below to view entire table
# pd.set_option('display.max_rows', None) 
# pd.set_option('display.max_columns', None) 


print("Summary Results Table:")
print(df_new)
