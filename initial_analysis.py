# Part 2- Initial Analysis- Data Overview
import sqlite3
import pandas as pd


def initial_analysis():
    connection = sqlite3.connect("cell-count.db")

    # Query SQL for samples table
    df = pd.read_sql(
        "SELECT sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte FROM Samples;",
        connection,
    )

    # Calcuate totals for each row
    df["total_count"] = (
        df["b_cell"]
        + df["cd8_t_cell"]
        + df["cd4_t_cell"]
        + df["nk_cell"]
        + df["monocyte"]
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

    # Add results to database
    connection = sqlite3.connect("cell-count.db")
    cursor = connection.cursor()

    table_creation = [
        """CREATE TABLE IF NOT EXISTS Summary (
        id INTEGER PRIMARY KEY, 
        sample text NOT NULL, 
        total_count INTEGER NOT NULL,
        population text NOT NULL,
        count INTEGER NOT NULL,
        percentage REAL NOT NULL,
        sample_id INTEGER NOT NULL,
        FOREIGN KEY (sample) REFERENCES Samples(sample_id)
    );""",
    ]

    try:
        for table in table_creation:
            cursor.execute(table)
        print("Tables Created")
    except sqlite3.OperationalError as error:
        print(error)

    # Clean tables
    connection.execute("DELETE FROM Summary;")

    # Insert data into database
    summary_df = df_new.drop_duplicates()
    samples_db = pd.read_sql("SELECT * FROM Samples", connection)  # get foreign key
    samples_table = samples_db[["sample", "sample_id"]].drop_duplicates()
    summary_merged = summary_df.merge(samples_table, on=["sample"])  # merge

    summary_merged.to_sql("Summary", connection, if_exists="append", index=False)
    connection.commit()


if __name__ == "__main__":
    initial_analysis()
