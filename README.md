# 1. Instructions to Run Code
1. Ensure all packages/dependencies are installed correctly using requirements.txt.<br> 
Run the following command: <br> 
```pip install -r requirements.txt``` <br> 
2. (Optional) Delete cell-count.db, boxplot_yes.png, and boxplot_no.png as this will be reproduced when running app.py. <br> 
3. Run app.py using the following command: <br> 
```streamlit run app.py``` <br> 
This will run all the necessary files and create the dashboard of results.
NOTE: Each analysis file can also be run independently by running the follow command:
```python <file.name>.py```

# 2. Relational Database Schema
The diagram below is a visual representation of the relational database schema created, with each box representing a table.  <br> 
<img width="981" height="915" alt="schema_diagram" src="https://github.com/user-attachments/assets/53bab787-80dd-48f4-a0ee-2d5314ec9590" /> <br> 

The 'Projects' table contains information specific to each project which is the project and sample_type. This way a new project can easily be added with its respective sample type.  <br> 
Each project has a number of subjects, so the 'Subjects' table maps back to the 'Projects' table using project_id as a key.  <br> 
The 'Subjects' table contains all information about each subject that would be recorded at intake: subject, condition, age, sex. This makes it easy to add new Subjects when they are first enrolled.  <br> 
The 'Treatments' table contains information regarding treatment and response for each patient, mapped back to the subject table by subject_id. Because this information would not be available at intake, creating a separate table allows for streamlined analysis of results once they become available. <br> 
The 'Samples' table contains information regarding sample, time_from_treatment_start, and all of the cell values. It is mapped back to the 'Subjects' table using subject_id as a key. This was done because each patient has three samples, allowing for easy mapping from patient to sample, while separating information that remains consistent for each patient. <br> 
Overall, this database structure allows for ease of analysis even with many more projects, subjects, and samples included. It separates the datas into tables based on considerations like availability of information at a certain time, as well as additional subjects, samples, or projects being added.
