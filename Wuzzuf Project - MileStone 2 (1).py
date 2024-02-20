#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install Selenium


# In[2]:


pip install webdriver-manager


# In[ ]:


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()  

# this code spans all pages of job postings and saves the href for each job posting to an excel file
# since each page of postings has the same url with only a different number at the end, we will use a loop to create
# a list of the urls and then use it to get the href
base_url = "https://wuzzuf.net/a/IT-Software-Development-Jobs-in-Egypt?ref=browse-jobs&start="
page_urls = [base_url + str(start) for start in range(70)]

href_list = [] 

for url in page_urls:
    driver.get(url)
    driver.implicitly_wait(10)     # waits for page to load
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    links_with_class = soup.find_all('a', class_='css-o171kl')

    for link in links_with_class:
        href = link.get('href')
        if href and href.startswith('http'):
            href_list.append(href) 

driver.quit()


df = pd.DataFrame({"Href": href_list})   # storing as pandas df to convert to excel


output_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\job_info.xlsx"
df.to_excel(output_file_path, index=False)

print("Data has been successfully scraped and Job Posting Links are now in the Excel file.")


# In[1]:


import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# This code will open the Job Posting URLs from the excel file and extract the data for each job, saving it to an excel file
input_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\job_info.xlsx"
df = pd.read_excel(input_file_path)
urls = df['Href'].tolist()


driver = webdriver.Chrome()

data = []
skills_data = []
company_href_data = []
job_categories_data = []
company_href_set = set()

for url in urls:
    driver.get(url)
    driver.implicitly_wait(10)
    current_url = driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # if any item is missing in the page, it is stored as 'N/A'
    title_element = soup.select_one('#app > div > main > article > section.css-dy1y6u > div > h1')
    title = title_element.text if title_element else 'N/A'

    experience_element = soup.select_one('#app > div > main > article > section.css-3kx5e2 > div:nth-child(2) > span.css-47jx3m > span')
    experience_needed = experience_element.text if experience_element else 'N/A'

    career_element = soup.select_one('#app > div > main > article > section.css-3kx5e2 > div:nth-child(3) > span.css-47jx3m > span')
    career_level = career_element.text if career_element else 'N/A'

    education_element = soup.select_one('#app > div > main > article > section.css-3kx5e2 > div:nth-child(4) > span.css-47jx3m > span')
    education_level = education_element.text if education_element else 'N/A'

    salary_element = soup.select_one('#app > div > main > article > section.css-3kx5e2 > div:nth-child(5) > span.css-47jx3m > span')
    salary = salary_element.text if salary_element and salary_element.text != 'Confidential' else 'N/A'

    job_description_element = soup.select_one('#app > div > main > article > section:nth-child(4) > div')
    job_description = job_description_element.text if job_description_element else 'N/A'
    
# the code for company href stores the href in a set, which is later to be used to create a list of unique company hrefs
# to store the urls for all companies on Wuzzuf that posted jobs for IT/Software Development, but only store the link for
# each company once
    company_name_element = soup.select_one('#app > div > main > article > section.css-dy1y6u > div > strong > div > a')
    company_name = company_name_element.text if company_name_element else 'N/A'
    company_href_element = soup.select_one('#app > div > main > article > section.css-dy1y6u > div > strong > div > a')
    company_href = company_href_element['href'] if company_href_element else 'N/A'
    company_href_set.add(company_href)
    
    
    

    company_sector = 'IT/Software Development' # a placeholder until we scrape the companies and find their sector

    # skills and categoires are stored in separate arrays as they are to be written to a separate excel sheet 
    # with the Job and one skill in each row
    skills_element = soup.select('#app > div > main > article > section.css-3kx5e2 > div.css-s2o0yh a')
    skills = [skill.text for skill in skills_element]
    
    for skill in skills:
        skills_data.append([company_name, company_sector, title, skill])

    
    job_categories_element = soup.select('#app > div > main > article > section.css-3kx5e2 > div.css-13sf2ik ul li')
    job_categories = [category.text for category in job_categories_element]
    
    for category in job_categories:
        job_categories_data.append([company_name, company_sector, title, category])

    data.append([title, experience_needed, career_level, education_level, salary, job_description, company_name, company_sector])


driver.quit()

# Job Info converted to pandas df to save to excel sheet
df = pd.DataFrame(data, columns=["Title", "Experience_Needed", "Career_Level", "Education_Level", "Salary", "Job_Description", "Company_Name", "Company_Sector"])


output_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\Job_postings.xlsx"
df.to_excel(output_file_path, index=False)

# Skills converted to pandas df to save to excel sheet
skills_df = pd.DataFrame(skills_data, columns=["Company_Name", "Company_Sector", "Title", "Skill"])


skills_output_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\Job_Skills.xlsx"
skills_df.to_excel(skills_output_file_path, index=False)

# Job categories converted to pandas df to save to excel sheet
job_categories_df = pd.DataFrame(job_categories_data, columns=["Company_Name", "Company_Sector", "Title", "Category"])


job_categories_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\Job_Categories.xlsx"
job_categories_df.to_excel(job_categories_path, index=False)

# Company Href converted to pandas df to save to excel sheet
unique_href = list(company_href_set)
company_href_df = pd.DataFrame(unique_href, columns=["Company_Href"])


company_href_output_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\Company_Href.xlsx"
company_href_df.to_excel(company_href_output_file_path, index=False)

print("Data has been scraped and saved to Excel files.")


# In[2]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException  # Import WebDriverException for handling invalid URLs
from bs4 import BeautifulSoup

# The code reads company URLs from the Excel file they were saved to and retrieves their data
input_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\Company_Href.xlsx"
df = pd.read_excel(input_file_path)
company_urls = df['Company_Href'].tolist() 

driver = webdriver.Chrome()

data = []

for url in company_urls:
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        current_url = driver.current_url
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        name_element = soup.select_one('#app > div > div:nth-child(3) > div > div > div.css-12e2e2p > div.css-1eoy87d > h1')
        name = name_element.text if name_element else 'N/A'

        sector_element = soup.select_one('#app > div > div:nth-child(3) > div > div > div.css-12e2e2p > p > span:nth-child(1) > a')
        sector = sector_element.text if sector_element else 'N/A'

        location_element = soup.select_one('#profile-section > div > span:nth-child(1) > span.css-16heon9')
        location = location_element.text if location_element else 'N/A'

        foundation_date_element = soup.select_one('#profile-section > div > span:nth-child(2) > span.css-6whuzn')
        foundation_date = foundation_date_element.text if foundation_date_element else 'N/A'

        size_element = soup.select_one('#profile-section > div > span:nth-child(4) > span.css-16heon9')
        size = size_element.text if size_element else 'N/A'

        try:
            description_element = driver.find_element(By.CSS_SELECTOR, '#profile-section > p')
            description = description_element.text.strip()

            # This part of the code is used to click the 'See More' button if it is there, to read the full description
            see_more_button = driver.find_elements(By.CSS_SELECTOR, '#profile-section > p > span')
            if see_more_button:
                see_more_button[0].click()
                WebDriverWait(driver, 10).until(EC.invisibility_of_element(see_more_button[0]))
                description_element = driver.find_element(By.CSS_SELECTOR, '#profile-section > p')
                description = description_element.text.strip()

                # If see more is clicked, we must remove 'See Less' from the description
                if description.endswith("See Less"):
                    description = description.rsplit("See Less", 1)[0].strip()
        except NoSuchElementException:
            description = 'N/A'

        company_url_element = soup.select_one('#app > div > div:nth-child(3) > div > div > div.css-12e2e2p > div.css-aqnjlk > div > a')
        company_url = company_url_element['href'] if company_url_element else 'N/A'

        data.append([name, sector, location, foundation_date, size, description, company_url])
    except WebDriverException:
        print(f"Skipping invalid URL: {url}")

driver.quit()

# Data stored as pandas df to convert to an Excel file
df = pd.DataFrame(data, columns=["Name", "Sector", "Location", "Foundation_Date", "Size", "Description", "URL"])

output_file_path = r"C:\Users\shoai\OneDrive\Desktop\AUC\Fall 2023\Fundamentals of DB Systems\Milestone2\Company_Data.xlsx"
df.to_excel(output_file_path, index=False)

print("Company data has been scraped and saved to the Company_Data Excel file.")


# In[4]:


import pandas as pd

# Code to filter out Jobs with companies that are not in the company csv table

company_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Company_Data.csv"
job_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Job_postings.csv"


company_data = pd.read_csv(company_data_path, encoding='UTF-8') 
job_data = pd.read_csv(job_data_path, encoding='UTF-8')  


filtered_job_data = job_data[job_data['Company_Name'].isin(company_data['Name'])]


filtered_job_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Filtered_Job_postings.csv"


filtered_job_data.to_csv(filtered_job_data_path, index=False)

print(f"Filtered job data saved to: {filtered_job_data_path}")


# In[6]:


pip install faker


# In[8]:


import pandas as pd
from faker import Faker
import random

# Code to generate users

fake = Faker()


num_users = 500
users = []

for _ in range(num_users):
    username = fake.unique.user_name()  
    email = fake.email()
    gender = fake.random_element(elements=('Male', 'Female'))
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70)
    gpa = round(random.uniform(2.0, 4.0), 2) 

    users.append([username, email, gender, birthdate, gpa])


df = pd.DataFrame(users, columns=["Username", "Email", "Gender", "Birthdate", "GPA"])

# CSV file for users
df.to_csv(r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\User_Data.csv", index=False)

print("Random users saved to User_Data.csv")


# In[14]:


import pandas as pd
import random
# Code to generate skills for users 

skills = [
    "Communication",
    "Problem-Solving",
    "Time Management",
    "Flexibility",
    "Critical Thinking",
    "Creativity",
    "Collaboration",
    "Multicultural Sensitivity",
]

# CSV File for users
excel_file_path = r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\User_Data.csv'


df = pd.read_csv(excel_file_path)


usernames = df['Username'].tolist()


user_skills_data = []

# Generating 1-5 skills per user
for username in usernames:
    num_skills = random.randint(1, 5)
    user_skills = random.sample(skills, num_skills)
    for skill in user_skills:
        user_skills_data.append([username, skill])


user_skills_df = pd.DataFrame(user_skills_data, columns=['Username', 'Skill'])

# CSV file to store the user and skills
user_skills_file_path = r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\User_Skills.csv'


user_skills_df.to_csv(user_skills_file_path, index=False)

print(f"User skills have been saved to '{user_skills_file_path}'.")


# In[21]:


import pandas as pd

# Load the original job_postings and filtered_job_postings CSV files
company_file = "C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Company_Data.csv"
filtered_job_postings_file = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Filtered_Job_postings.csv"

# Read the CSV files into DataFrames
company_df = pd.read_csv(company_file)
filtered_job_postings_df = pd.read_csv(filtered_job_postings_file)

# Specify the column name you want to compare
column_name = "Company_Name"  # Change this to the name of the column you want to compare

# Compare the specified column between the two DataFrames
differences = filtered_job_postings_df[~filtered_job_postings_df["Company_Name"].isin(company_df["Name"])]

# Check if there are any differences
if differences.empty:
    print(f"No differences found in column '{column_name}'.")
else:
    print(f"Differences found in column '{column_name}':")
    print(differences)


# In[33]:


import pandas as pd

# Code to filter out Job Categories without a corresponding Company Name in the Company relation

company_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Company_Data.csv"
job_categories_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Job_Categories.csv"

company_data = pd.read_csv(company_data_path, encoding='UTF-8')
job_categories = pd.read_csv(job_categories_path, encoding='UTF-8')


unique_company_names = company_data['Name'].unique()


filtered_job_categories = job_categories[job_categories['Company_Name'].isin(unique_company_names)]

filtered_job_categories_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Filtered_Job_Categories.csv"

filtered_job_categories.to_csv(filtered_job_categories_path, index=False)

print(f"Filtered job categories data saved to: {filtered_job_categories_path}")


# In[34]:


import pandas as pd

# Code to filter out Job Skills without a corresponding Company Name in the Company relation

company_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Company_Data.csv"
job_skills_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Job_Skills.csv"

company_data = pd.read_csv(company_data_path, encoding='UTF-8')
job_skills = pd.read_csv(job_categories_path, encoding='UTF-8')


unique_company_names = company_data['Name'].unique()


filtered_job_skills = job_categories[job_skills['Company_Name'].isin(unique_company_names)]

filtered_job_skills_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Filtered_Job_Skills.csv"

filtered_job_skills.to_csv(filtered_job_skills_path, index=False)

print(f"Filtered job skills data saved to: {filtered_job_skills_path}")


# In[62]:


import pandas as pd
import random
from datetime import datetime, timedelta

# Load job data
job_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Filtered_Job_postings.csv"
job_data = pd.read_csv(job_data_path, encoding='UTF-8')

# Load user data
user_data_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\User_Data.csv"
user_data = pd.read_csv(user_data_path, encoding='UTF-8')

# Load user skills data
user_skills_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\User_Skills.csv"
user_skills_data = pd.read_csv(user_skills_path, encoding='UTF-8')

# Create an empty list to store the fake applications
fake_applications = []

# Define the date range
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 11, 30)

# Iterate through user data to generate fake applications
for _, user in user_data.iterrows():
    job_index = random.randint(0, len(job_data) - 1)
    username = user['Username']
    selected_job = job_data.loc[job_index, 'Title']
    selected_company = job_data.loc[job_index, 'Company_Name']
    
    # Generate a random date within the defined range
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    # Find the skills for the current user
    user_skills = user_skills_data[user_skills_data['Username'] == username]['Skill'].tolist()
    
    # Create the skills string
    skills_string = ', '.join(user_skills)
    
    # Create the cover letter using the template
    cover_letter = f'''I'm delighted to apply to the "{selected_job}" position at "{selected_company}". It is a wonderful match for my skills and career priorities, and as an experienced candidate in the field, I believe I have much to offer the "{selected_company}" team.In addition to the experience I have gathered within the field, I gained several skills that place me as a suitable candidate for this position. Some of these skills are {skills_string}.I'd be excited to bring my deep knowledge in this area to help "{selected_company}" achieve first-rate results.Please feel free to contact me at "{user['Email']}". Thank you for your time and consideration.'''
    
    # Create a fake application with the selected job, company, random date, and cover letter
    fake_application = {
        'Username': username,
        'Company_Name': selected_company,
        'Job_Title': selected_job,
        'Application_Date': random_date.strftime('%Y-%m-%d'),
        'CoverLetter': cover_letter
    }
        
    fake_applications.append(fake_application)
    
# Create a DataFrame from the list of fake applications
fake_applications_df = pd.DataFrame(fake_applications)

# Save the fake applications to a CSV file
fake_applications_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\wuzzuf\Fake_Applications.csv"
fake_applications_df.to_csv(fake_applications_path, index=False)

print(f"Fake applications saved to: {fake_applications_path}")


# In[ ]:




