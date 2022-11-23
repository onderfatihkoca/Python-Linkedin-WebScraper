from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector
import time
#import numpy as np

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "selenium_test"
)
mycursor = db.cursor()

driver = webdriver.Chrome("C:\Drivers\chromedriver")
class Linkedin:
    def __init__(self, job, location):
        self.job = job
        self.location = location
    
    def search(self): #Linkedin'deki iş ve şehir seçimini yaparak arama yapar
        driver.get("https://www.linkedin.com/jobs")
        driver.maximize_window()

        time.sleep(2)
        name_Input = driver.find_element("name", "keywords")
        name_Input.send_keys(self.job)
    
        location_Input = driver.find_element("name", "location")
        location_Input.clear()
        location_Input.send_keys(self.location)
        location_Input.send_keys(Keys.ENTER)

    def jobList(self): #Linkedin'deki iş ilanlarının verilerini çeker.
        time.sleep(3)

        for x in range (10): #Bütün ilanların yüklenebilmesi için sayfayı en aşağı çeker.
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
        
        job_Titles = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list h3")
        job_Locations = driver.find_elements(By.CSS_SELECTOR, ".job-search-card__location")
        job_CompanyNames = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list h4")
        job_PostDates = []
            
        for x in range (len(job_Titles)):
            print(f"[{x+1}]:")
            print(job_Titles[x].text)
            print(job_Locations[x].text)
            print(job_CompanyNames[x].text)
            y = x + 1
            try:
                a = driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/div/div[2]/div/time').text
                job_PostDates.append(a)
                print(driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/div/div[2]/div/time').text)
            except:       
                b = (driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/a/div[2]/div/time').text)
                job_PostDates.append(b)
                print(driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{y}]/a/div[2]/div/time').text)         

            print("\n")
            mycursor.execute(f"INSERT INTO jobs (title, location, company_name, post_date) VALUES ('{job_Titles[x].text}', '{job_Locations[x].text}', '{job_CompanyNames[x].text}', '{job_PostDates[x]}');")
            db.commit()            

        job_Type = NULL
        job_Description = NULL
        click_Count = 1

        #Sıra ile iş ilanlarına tıklar ve içerisindeki çeşitli verileri alır
        for click in range (50):
            try:
                driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/div/a').click()
            except:
                try:
                    driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/a').click()
                except:
                    break
                 
            #İlan içerisindeki "Tam Zamanlı/Yarı Zamanlı/Stajyer" bilgisini çeker. 
            j = 0
            while(True):
                time.sleep(0.5)
                try:
                    job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
                except:   

                    try:
                        job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span').text                                   
                    except:
                        job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section/div/ul/li/span').text
                
                if(job_Type != ""):
                    try:
                        job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text
                    except:
                        job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]/section/div').text
                    break
                j = j + 1
                if(j > 5):
                    try:
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count-1}]/div/a').click()
                        time.sleep(1)
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/div/a').click()
                        
                        time.sleep(0.5)
                        try:
                            job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
                        except:   

                            try:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span').text                                   
                            except:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section/div/ul/li/span').text
                        
                        if(job_Type != ""):
                            try:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text
                                if(job_Type != ""):
                                    break
                            except:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]/section/div').text
                            break
                        
                    except:
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count-1}]/a').click() 
                        time.sleep(1)
                        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{click_Count}]/div/a').click()
                        
                        time.sleep(0.5)
                        try:
                            job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span').text
                        except:   

                            try:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span').text                                   
                            except:
                                job_Type = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section/div/ul/li/span').text
                        
                        if(job_Type != ""):
                            try:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text
                            except:
                                job_Description = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]/section/div').text
                            break
                        
            job_Description = job_Description.replace('"', "'")
            mycursor.execute(f'UPDATE jobs SET description = "{job_Description}" WHERE id = {click_Count};')
            db.commit() 
            mycursor.execute(f"UPDATE jobs SET job_type = '{job_Type}' WHERE id = {click_Count};")
            db.commit()         
            print(f"[{click_Count}]: {job_Type}")
            print(f"[{click_Count}]: {job_Description[:300]}...")
 
            click_Count += 1

start = time.time()

linkedin = Linkedin("c++", "istanbul")
linkedin.search()
linkedin.jobList() 

end = time.time()    
print(f"\nExecution time: {end - start}")