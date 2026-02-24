# Part 4 Data Subset Analysis
import sqlite3
import pandas as pd


def subset_analysis():
    connection = sqlite3.connect("cell-count.db")

    # Query SQL

    # Determine how many melanoma PBMC miraclib baseline samples in each project
    project_count = pd.read_sql(
        """
        SELECT p.project, COUNT(*) AS count
        FROM Samples AS m
        JOIN Subjects as s ON m.subject_id = s.subject_id
        JOIN Treatments AS t ON s.subject_id = t.subject_id
        JOIN Projects AS p ON p.project_id = s.project_id
        WHERE s.condition = 'melanoma' AND t.treatment = 'miraclib' AND p.sample_type = 'PBMC' AND m.time_from_treatment_start = '0'
        GROUP BY p.project
        """,
        connection,
    )

    print(project_count)

    # Determine how many melanoma PBMC miraclib subjects at baseline were responders/non-responders
    response_count = pd.read_sql(
        """
        SELECT t.response, COUNT(*) AS count
        FROM Samples AS m
        JOIN Subjects as s ON m.subject_id = s.subject_id
        JOIN Treatments AS t ON s.subject_id = t.subject_id
        JOIN Projects AS p ON p.project_id = s.project_id
        WHERE s.condition = 'melanoma' AND t.treatment = 'miraclib' AND p.sample_type = 'PBMC' AND m.time_from_treatment_start = '0'
        GROUP BY t.response
        """,
        connection,
    )

    print(response_count)

    # Determine how many melanoma PBMC miraclib subjects at baseline were male/female
    sex_count = pd.read_sql(
        """
        SELECT s.sex, COUNT(*) AS count
        FROM Samples AS m
        JOIN Subjects as s ON m.subject_id = s.subject_id
        JOIN Treatments AS t ON s.subject_id = t.subject_id
        JOIN Projects AS p ON p.project_id = s.project_id
        WHERE s.condition = 'melanoma' AND t.treatment = 'miraclib' AND p.sample_type = 'PBMC' AND m.time_from_treatment_start = '0'
        GROUP BY s.sex
        """,
        connection,
    )

    print(sex_count)
    return project_count, response_count, sex_count


if __name__ == "__main__":
    subset_analysis()
