from selenium import webdriver
from selenium.webdriver.common.by import By
import math
import pandas as pd


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

job_info = []
jobs_pages = []
job_details = []
page_no = 0

websiteURL = f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_no}"
driver.get(websiteURL)
# count the limit pages that each page has 16 job offor
limit_pages = math.ceil(float(driver.find_element(By.TAG_NAME,'strong').text) / 16)

while(page_no <= limit_pages):
    driver.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_no}")
    # get all jobs info
    titles = driver.find_elements(By.CLASS_NAME,"css-m604qf")
    company_names = driver.find_elements(By.CLASS_NAME,"css-d7j1kk")
    locations = driver.find_elements(By.CLASS_NAME,"css-5wys0k")
    dates_of_publication = driver.find_elements(By.CLASS_NAME,"css-d7j1kk")
    jobs_skills = driver.find_elements(By.CLASS_NAME,"css-y4udm8")
    
    for i in range(len(titles)):
        # Get more information by accessing the job page
        # every job title has link to jop page for more information
        jobs_pages.append(titles[i].find_element(By.CLASS_NAME,"css-o171kl").get_attribute("href"))  
        
        job_info.append({
            "Title" : titles[i].text.strip(),
            "Company Name" : company_names[i].text.replace("-","").strip(),
            "Location" : locations[i].text.strip(),
            "Date Of Puplication" : dates_of_publication[i].find_element(By.TAG_NAME,"div").text.strip(),
            "skills" : jobs_skills[i].text.strip(),
            })
    page_no +=1

# search every job page 
for link in jobs_pages:
    driver.get(link)
    is_requirements = len(driver.find_elements(By.CLASS_NAME,'css-1t5f0fr')) > 0 
    requirements = driver.find_element(By.CLASS_NAME,'css-1t5f0fr').text if is_requirements else "Null"
    salary = driver.find_elements(By.CLASS_NAME,'css-4xky9y')[3].text 
    job_details.append({
        "Salary" : salary,
        "Requirements" : requirements,
    })

all_job_info = [{**x,**y} for x,y in zip(job_info,job_details)]

# save info to csv file
df = pd.DataFrame(all_job_info)
df.to_csv("jobInfo.csv")
