# Part 3: Statistical Analysis
import sqlite3
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def statistical_analysis():
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
    print(join)

    # Create separate dataframe for each response
    df_yes = join[join["response"] == "yes"]
    df_no = join[join["response"] == "no"]

    # Calculate Degrees of Freedom
    degree = len(df_yes) + len(df_no) - 2
    print(degree)

    cell_types = join["population"].unique()  # determine all cell_types
    results = []

    for cell in cell_types:
        group_yes = df_yes[df_yes["population"] == cell]["percentage"]
        group_no = df_no[df_no["population"] == cell]["percentage"]

        # Independent t-test (Welch's)
        t_stat, t_p = stats.ttest_ind(group_yes, group_no, equal_var=False)

        results.append({"cell_type": cell, "t_stat": t_stat, "t_p": t_p})

    results_df = pd.DataFrame(results)

    # Create boxplots for yes/no response
    df_yes.boxplot(column="percentage", by="population", grid=False)
    plt.title("Relative Frequency for 'Yes' Response ")
    plt.suptitle("")
    plt.xlabel("Cell Population ")
    plt.ylabel("Percentage")
    plt.savefig("boxplot_yes.png", dpi=300)

    plt.clf()
    df_no.boxplot(column="percentage", by="population", grid=False)
    plt.title("Relative Frequency for 'No' Response ")
    plt.suptitle("")
    plt.xlabel("Cell Population ")
    plt.ylabel("Percentage")
    plt.savefig("boxplot_no.png", dpi=300)

    return results_df


if __name__ == "__main__":
    statistical_analysis()
