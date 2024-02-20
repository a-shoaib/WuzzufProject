import mysql.connector
import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

db_config = {
    "host": "sql8.freemysqlhosting.net",
    "user": "sql8662930",
    "password": "YbmFNKSlb8",
    "database": "sql8662930"
}

# Function to handle opening different screens
def open_screen(screen_name):
    if screen_name == "Register a User":
        register_user_screen()
    elif screen_name == "Add a New User Application":
        add_user_application_screen()
    elif screen_name == "Show All Job Postings for a Given Sector":
        jobs_by_sector_screen()
    elif screen_name == "Show All Job Postings for a Given Set of Skills":
        show_jobs_by_skills_screen()
    elif screen_name == "Show the Top 5 Sectors by Number of Job Posts":
        show_top_sectors()
    elif screen_name == "Show the Top 5 Skills in High Demand":
        show_top_skills()
    elif screen_name == "Show the Top 5 Growing Startups in Egypt":
        show_growing_startups()
    elif screen_name == "Show the Top 5 Most Paying Companies in Egypt":
        show_most_paying_companies()
    elif screen_name == "Show All Postings for a Given Company":
        get_company_and_show_postings()
    elif screen_name =="Show the Top 5 Categories by Volume of Postings":
        show_top_categories()
    else:
        messagebox.showinfo("Info", f"{screen_name} screen is not implemented yet.")

# START OF QUERY 1
def register_user_screen():
    global username_entry, email_entry, gender_var, birthdate_entry, gpa_entry

    register_window = tk.Toplevel(root)
    register_window.title("Register a User")

   
    username_label = tk.Label(register_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    email_label = tk.Label(register_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(register_window)
    email_entry.pack()


    gender_label = tk.Label(register_window, text="Gender:")
    gender_label.pack()
    gender_var = tk.StringVar()
    gender_radio1 = tk.Radiobutton(register_window, text="Male", variable=gender_var, value="M")
    gender_radio2 = tk.Radiobutton(register_window, text="Female", variable=gender_var, value="F")
    gender_radio1.pack()
    gender_radio2.pack()

    
    birthdate_label = tk.Label(register_window, text="Birthdate (YYYY-MM-DD):")
    birthdate_label.pack()
    birthdate_entry = tk.Entry(register_window)
    birthdate_entry.pack()

    
    gpa_label = tk.Label(register_window, text="GPA:")
    gpa_label.pack()
    gpa_entry = tk.Entry(register_window)
    gpa_entry.pack()

    
    submit_button = tk.Button(register_window, text="Submit", command=submit_user_form)
    submit_button.pack()
def submit_user_form():
    
    username = username_entry.get()
    email = email_entry.get()
    gender = gender_var.get()
    birthdate = birthdate_entry.get()
    gpa = gpa_entry.get()

    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE Username = %s", (username,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "Username already exists.")
            return

        
        sql = "INSERT INTO users (Username, Email, Gender, Birthdate, GPA) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (username, email, gender, birthdate, gpa))
        conn.commit()

        messagebox.showinfo("Success", "User registered successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 1

# START OF QUERY 2
def add_user_application_screen():
    global username_entry_app, job_title_entry, company_name_entry, application_date_entry

    application_window = tk.Toplevel(root)
    application_window.title("Add New User Application")

   
    username_label_app = tk.Label(application_window, text="Username:")
    username_label_app.pack()
    username_entry_app = tk.Entry(application_window)
    username_entry_app.pack()

 
    job_title_label = tk.Label(application_window, text="Job Title:")
    job_title_label.pack()
    job_title_entry = tk.Entry(application_window)
    job_title_entry.pack()

    company_name_label = tk.Label(application_window, text="Company Name:")
    company_name_label.pack()
    company_name_entry = tk.Entry(application_window)
    company_name_entry.pack()


    application_date_label = tk.Label(application_window, text="Application Date (YYYY-MM-DD):")
    application_date_label.pack()
    application_date_entry = tk.Entry(application_window)
    application_date_entry.pack()

   
    submit_button_app = tk.Button(application_window, text="Submit", command=submit_application_form)
    submit_button_app.pack()
def submit_application_form():
    
    username = username_entry_app.get()
    job_title = job_title_entry.get()
    company_name = company_name_entry.get()
    application_date = application_date_entry.get()


    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE Username = %s", (username,))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Error","Username does not exist.")
            return
        
        # Check if the job title and company name exist in the 'job' table
        cursor.execute("SELECT COUNT(*) FROM job WHERE Title = %s AND Company = %s", (job_title, company_name))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Error","There are no vacancies for the given job")
            return
        
        # Check for existing application
        cursor.execute("SELECT COUNT(*) FROM userappliesforjob WHERE Username = %s AND Job_Title = %s AND Company_Name = %s",
                         (username, job_title, company_name))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "Application for this job by this user already exists")
            return
        
        

        insert_sql = "INSERT INTO userappliesforjob (Username, Job_Title, Company_Name, Application_Date) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_sql, (username, job_title, company_name, application_date))
        conn.commit()
        print("Application submitted successfully.")

        messagebox.showinfo("Success", "Application submitted successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 2

# START OF QUERY 3
def jobs_by_sector_screen():
    global sector_entry_app

    job_by_sector_window = tk.Toplevel(root)
    job_by_sector_window.title("Show Jobs by Sector")

    sector_label_app = tk.Label(job_by_sector_window, text="Choose Sector:")
    sector_label_app.pack()
    sector_entry_app = tk.Entry(job_by_sector_window)
    sector_entry_app.pack()

    submit_button_app = tk.Button(job_by_sector_window, text="Submit", command=display_jobs_by_sector)
    submit_button_app.pack()
def display_jobs_by_sector():
    sector = sector_entry_app.get()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "SELECT job.Title, job.Experience_Needed, job.Career_Level, job.Education_Level, job.Salary, job.Job_Description, job.Company FROM job INNER JOIN company ON job.Company = company.Company_Name WHERE company.Sector = %s"
        cursor.execute(sql, (sector,))
        jobs = cursor.fetchall()

        result_window = tk.Toplevel(root)
        result_window.title("Job Postings")

       
        result_text = tk.Text(result_window, wrap='word')
        result_text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(result_window, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text['yscrollcommand'] = scrollbar.set

        if jobs:
            for job in jobs:
                job_info = (f"Title: {job[0]}\nExperience Needed: {job[1]}\nCareer Level: {job[2]}\n"
                            f"Education Level: {job[3]}\nSalary: {job[4]}\nDescription: {job[5]}\n"
                            f"Company: {job[6]}\n\n")
                result_text.insert('end', job_info)
            result_text.config(state='disabled')  
        else:
            result_text.insert('end', "No job postings found for this sector.")
            result_text.config(state='disabled')  
            

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 3


# START OF QUERY 4
def show_jobs_by_skills_screen():
    skills_window = tk.Toplevel(root)
    skills_window.title("Show Job Postings by Skills")

   
    skills_entry = tk.Entry(skills_window)

    
    tk.Label(skills_window, text="Enter skills separated by commas:").pack()
    skills_entry.pack()

    
    submit_button = tk.Button(skills_window, text="Show Jobs", command=lambda: show_jobs(
        skills_entry.get().split(',')
    ))
    submit_button.pack()
def show_jobs(skills_list):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        like_patterns = ["%" + skill + "%" for skill in skills_list]

        sql = """
        SELECT DISTINCT job.Title, job.Experience_Needed, job.Career_Level, job.Education_Level,
                        job.Salary, job.Job_Description, job.Company
        FROM job
        INNER JOIN job_skills ON job.Title = job_skills.Job_Title AND job.Company_Name = job_skills.Company_Name
        WHERE """
        
       
        like_clauses = ' OR '.join(f"job_skills.Skill LIKE %s" for _ in skills_list)
        sql += like_clauses
        
        cursor.execute(sql, like_patterns)
        jobs = cursor.fetchall()
        
        result_window = tk.Toplevel(root)
        result_window.title("Job Postings")

        
        result_text = tk.Text(result_window, wrap='word')
        result_text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(result_window, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text['yscrollcommand'] = scrollbar.set

        if jobs:
            for job in jobs:
                job_info = (f"Title: {job[0]}\nExperience Needed: {job[1]}\nCareer Level: {job[2]}\n"
                            f"Education Level: {job[3]}\nSalary: {job[4]}\nDescription: {job[5]}\n"
                            f"Company: {job[6]}\n\n")
                result_text.insert('end', job_info)
            result_text.config(state='disabled')  

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 4

# START OF QUERY 5
def show_top_sectors():
    # Connect to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT company.Sector, COUNT(*) AS NumberOfJobs FROM job INNER JOIN company ON job.Company_Name = company.Company_Name GROUP BY company.Sector ORDER BY NumberOfJobs DESC LIMIT 5"
        cursor.execute(sql)
        results = cursor.fetchall()

        message = "Top 5 Sectors by Number of Job Posts:\n\n"
        for row in results:
            message += f"Sector: {row[0]}, Number of Jobs: {row[1]}\n"
        
        messagebox.showinfo("Top Sectors", message)
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 5

# START OF QUERY 6
def show_top_skills():

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        
        sql = "SELECT Skill, COUNT(*) AS Demand FROM job_skills GROUP BY Skill ORDER BY Demand DESC LIMIT 5"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        
        message = "Top 5 Skills in High Demand:\n\n"
        for row in results:
            message += f"Skill: {row[0]}, Demand: {row[1]}\n"
        
        
        messagebox.showinfo("Top Skills", message)
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 6

# START OF QUERY 7
def show_growing_startups():
    # Connect to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Your SQL query for function 7
        sql = """
        SELECT Company, COUNT(*) AS Vacancies, Foundation_Date
        FROM job
        INNER JOIN company ON job.Company = company.Company_Name
        WHERE company.Location = 'Egypt' AND company.Foundation_Date IS NOT NULL
        GROUP BY Company
        ORDER BY Vacancies DESC, Foundation_Date
        LIMIT 5
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Format the results into a string message
        message = "Top 5 Growing Startups in Egypt:\n\n"
        for row in results:
            message += f"Startup: {row[0]}, Vacancies: {row[1]}, Founded: {row[2]}\n"
        
        # Show the message in a messagebox
        messagebox.showinfo("Growing Startups", message)
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 7

# START OF QUERY 8
def show_most_paying_companies():
    # Connect to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Your SQL query for function 8
        sql = """
        SELECT Company, AVG(Salary) AS AverageSalary
        FROM job
        INNER JOIN company ON job.Company = company.Company_Name
        WHERE company.Location = 'Egypt'
        GROUP BY Company
        ORDER BY AverageSalary DESC
        LIMIT 5
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Format the results into a string message
        message = "Top 5 Most Paying Companies in Egypt:\n\n"
        for row in results:
            message += f"Company: {row[0]}, Average Salary: {row[1]:.2f}\n"
        
        # Show the message in a messagebox
        messagebox.showinfo("Most Paying Companies", message)
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 8

# START OF QUERY 9
def get_company_and_show_postings():
    company_name = simpledialog.askstring("Input", "Enter the company name:")
    if company_name:
        show_postings_for_company(company_name)
    else:
        messagebox.showinfo("Cancelled", "You cancelled the input dialog.")
def show_postings_for_company(company_name):
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        
        sql = "SELECT job.Title, job.Experience_Needed, job.Career_Level,  job.Education_Level,  job.Salary, job.Job_Description, job.Company  FROM job WHERE Company_Name = %s"
        cursor.execute(sql, (company_name,))
        job_postings = cursor.fetchall()

        result_window = tk.Toplevel(root)
        result_window.title("Vacancies at this company are: ")
        
        result_text = tk.Text(result_window, wrap='word')
        result_text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(result_window, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text['yscrollcommand'] = scrollbar.set

        if job_postings:
            for job in job_postings:
                job_info = (f"Title: {job[0]}\nExperience Needed: {job[1]}\nCareer Level: {job[2]}\n"
                            f"Education Level: {job[3]}\nSalary: {job[4]}\nDescription: {job[5]}\n"
                            f"Company: {job[6]}\n\n")
                result_text.insert('end', job_info)
            result_text.config(state='disabled')  
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 9

# START OF QUERY 10
def show_top_categories():

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT Category
            FROM job_categories
            GROUP BY Category
            ORDER BY COUNT(*) DESC
            LIMIT 1
        """)
        top_category = cursor.fetchone()[0]
        
        # Get the next top 5 categories excluding the top category
        cursor.execute("""
            SELECT Category, COUNT(*) AS NumberOfPostings
            FROM job_categories
            WHERE Category != %s
            GROUP BY Category
            ORDER BY NumberOfPostings DESC
            LIMIT 5
        """, (top_category,))

        categories = cursor.fetchall()
        
        # Display the results
        if categories:
            output = "\n".join(f"Category: {category[0]}, Number of Postings: {category[1]}" for category in categories)
            messagebox.showinfo("Top 5 Categories (Excluding Highest)", output)
        else:
            messagebox.showinfo("Top 5 Categories (Excluding Highest)", "No categories found.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# END OF QUERY 10

######################################################

root = tk.Tk()
root.title("Job Portal")

# Job Portal label
title_label = tk.Label(root, text="JOB PORTAL", fg="blue", font=("Helvetica", 16))
title_label.pack(pady=10)

# Question label
question_label = tk.Label(root, text="What would you like to do?")
question_label.pack(pady=5)

# List of functions
functions = ["Register a User", "Add a New User Application", "Show All Job Postings for a Given Sector", "Show All Job Postings for a Given Set of Skills", "Show the Top 5 Sectors by Number of Job Posts", "Show the Top 5 Skills in High Demand", "Show the Top 5 Growing Startups in Egypt", "Show the Top 5 Most Paying Companies in Egypt", "Show All Postings for a Given Company", "Show the Top 5 Categories by Volume of Postings"]

# Create a button for each function
for function in functions:
    button = tk.Button(root, text=function, command=lambda f=function: open_screen(f))
    button.pack(pady=2)

# Start the application
root.mainloop()
