import sqlite3
import pandas as pd


def load_data():
    # Database Creation
    connection = sqlite3.connect("cell-count.db")
    cursor = connection.cursor()

    table_creation = [
        """CREATE TABLE IF NOT EXISTS Projects (
        project_id INTEGER PRIMARY KEY, 
        project text NOT NULL, 
        sample_type text NOT NULL
    );""",
        """CREATE TABLE IF NOT EXISTS Subjects (
        subject_id INTEGER PRIMARY KEY, 
        subject text NOT NULL, 
        condition text NOT NULL,
        age text NOT NULL,
        sex text NOT NULL,
        project_id INTEGER,
        FOREIGN KEY (project_id) REFERENCES Projects(project_id)
    );""",
        """CREATE TABLE IF NOT EXISTS Treatments (
        treatment_id INTEGER PRIMARY KEY, 
        treatment text NOT NULL, 
        response text,
        subject_id INTEGER,
        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
    );""",
        """CREATE TABLE IF NOT EXISTS Samples (
        sample_id INTEGER PRIMARY KEY, 
        sample text NOT NULL, 
        time_from_treatment_start INTEGER NOT NULL,
        b_cell INTEGER NOT NULL,
        cd8_t_cell INTEGER NOT NULL,
        cd4_t_cell INTEGER NOT NULL,
        nk_cell INTEGER NOT NULL,
        monocyte INTEGER NOT NULL,
        subject_id INTEGER,
        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
    );""",
    ]

    try:
        for table in table_creation:
            cursor.execute(table)
        print("Tables Created")
    except sqlite3.OperationalError as error:
        print(error)

    # Data insertion
    df = pd.read_csv("datasets/cell-count.csv")

    # Clean all tables
    connection.execute("DELETE FROM Subjects;")
    connection.execute("DELETE FROM Projects;")
    connection.execute("DELETE FROM Treatments;")
    connection.execute("DELETE FROM Samples;")
    connection.commit()

    connection.execute("PRAGMA foreign_keys = ON")  # prevents invalid foreign keys

    # Create table for Projects
    projects_df = df[["project", "sample_type"]].drop_duplicates()
    # Insert to database
    projects_df.to_sql("Projects", connection, if_exists="append", index=False)
    connection.commit()

    # Create table for Subjects
    subjects_df = df[
        ["subject", "condition", "age", "sex", "project", "sample_type"]
    ].drop_duplicates()
    projects_db = pd.read_sql("SELECT * FROM Projects", connection)  # get foreign key
    subjects_merged = subjects_df.merge(
        projects_db, on=["project", "sample_type"]
    )  # merge
    subjects_final_df = subjects_merged[
        ["subject", "condition", "age", "sex", "project_id"]
    ]
    # Insert to database
    subjects_final_df.to_sql("Subjects", connection, if_exists="append", index=False)
    connection.commit()

    # Create table for Treatments
    treatments_df = df[["treatment", "response", "subject"]].drop_duplicates()
    subjects_db = pd.read_sql("SELECT * FROM Subjects", connection)  # get foreign key
    treatments_merged = treatments_df.merge(subjects_db, on=["subject"])  # merge
    treatments_final_df = treatments_merged[["treatment", "response", "subject_id"]]
    # Insert to database
    treatments_final_df.to_sql(
        "Treatments", connection, if_exists="append", index=False
    )
    connection.commit()

    # Create table for Samples
    samples_df = df[
        [
            "sample",
            "time_from_treatment_start",
            "b_cell",
            "cd8_t_cell",
            "cd4_t_cell",
            "nk_cell",
            "monocyte",
            "subject",
        ]
    ].drop_duplicates()
    samples_merged = samples_df.merge(subjects_db, on=["subject"])  # merge
    samples_final_df = samples_merged[
        [
            "sample",
            "time_from_treatment_start",
            "b_cell",
            "cd8_t_cell",
            "cd4_t_cell",
            "nk_cell",
            "monocyte",
            "subject_id",
        ]
    ]
    # Insert to database
    samples_final_df.to_sql("Samples", connection, if_exists="append", index=False)
    connection.commit()


if __name__ == "__main__":
    load_data()
