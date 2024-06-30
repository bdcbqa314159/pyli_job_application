import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
from datetime import datetime

class LinkedInUrl:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("URL_LINKEDIN")
    
    def __call__(self):
        return self.url
    
class SetupDriver():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self._driver = webdriver.Chrome(options=chrome_options)

    @property
    def driver(self):
        return self._driver

class EnvLoader:
    def __init__(self):
        load_dotenv()
        self.account_email = os.getenv("ACCOUNT_EMAIL")
        self.account_password = os.getenv("ACCOUNT_PASSWORD")
        self.phone = os.getenv("PHONE")
    
    def __call__(self):
        return self.account_email, self.account_password, self.phone

class AbortApplication:
    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver
    
    def __call__(self):
        # Click Close Button
        close_button = self.driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_button.click()

        time.sleep(2)
        # Click Discard Button
        discard_button = self.driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
        discard_button.click()
        return

class NavigateUrl:
    def __init__(self, driver, url):
        self._driver = driver
        self._url = url

    @property
    def driver(self):
        return self._driver

    @property
    def url(self):  
        return self._url

    def __call__(self):
        self.driver.get(self.url)
        return
    
class KillSession:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver
    
    def __call__(self):
        time.sleep(5)
        self.driver.close()
        self.driver.quit()
        return
    
class CookiesDenial:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver
    
    def __call__(self):
        time.sleep(2)
        reject_button = self.driver.find_element(by=By.CSS_SELECTOR, value='button[action-type="DENY"]')
        reject_button.click()
        return
    
class SignIn:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver
    
    def __call__(self):
        time.sleep(2)
        sign_in_button = self.driver.find_element(by=By.LINK_TEXT, value="Sign in")
        sign_in_button.click()
        return

class ApplicationFilling:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver

    def __call__(self):
        time.sleep(5)
        env_vars = EnvLoader()
        abortApplication = AbortApplication(self.driver)
        account_email, account_password, phone_number = env_vars()
        email_field = self.driver.find_element(by=By.ID, value="username")
        password_field = self.driver.find_element(by=By.ID, value="password")

        email_field.send_keys(account_email)
        password_field.send_keys(account_password)
        password_field.send_keys(Keys.ENTER)
        print("CAPTCHA - Solve Puzzle Manually")
        input("Press Enter when you have solved the Captcha")

        time.sleep(5)
        
        apply_button = self.driver.find_element(by=By.LINK_TEXT, value="Jobs")
        apply_button.click()
        
        number = 100
        while True:

            id_job = f"jobs-search-box-keyword-id-ember{number}"
            id_loc = f"jobs-search-box-location-id-ember{number}"
            try:
                job_title_field = self.driver.find_element(by=By.ID, value=id_job)
                job_location_field = self.driver.find_element(by=By.ID, value=id_loc)
                job_title_field.send_keys("Design Graphique / Directeur Artisitique")
                job_location_field.send_keys("Paris")
                job_title_field.send_keys(Keys.ENTER)
            except:
                number+=1
                continue
            else:
                print(f"Job Title and Location Entered number:{number}")
                break
        
        job_listing = self.driver.find_element(by=By.CLASS_NAME, value="scaffold-layout__list-container")
        

        return job_listing
    
def test_function():
    linkedin_url = LinkedInUrl()
    url = linkedin_url()
    mySetup = SetupDriver()
    driver = mySetup.driver

    cookiesdenial = CookiesDenial(driver)
    signIn = SignIn(driver)
    applicationFilling = ApplicationFilling(driver)
    killer = KillSession(driver)
    navigate = NavigateUrl(driver, url)

    navigate()
    cookiesdenial()
    signIn()
    app = applicationFilling()
    print(app)
    # killer()
                
if __name__ == "__main__":
    print("working in progress dude")

    path = f'https://www.linkedin.com/jobs/search?keywords=Design%20Graphique&location=Paris&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    mySetup = SetupDriver()
    driver = mySetup.driver
    cookiesdenial = CookiesDenial(driver)
    navigate = NavigateUrl(driver, path)
    navigate()
    cookiesdenial()

    
    block = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/ul')
    job_list = block.find_elements(By.CLASS_NAME, 'base-card')
    current = len(job_list)

    while True:    # Create a loop
        html = driver.find_element(By.TAG_NAME,'html')
        html.send_keys(Keys.END)
        try:
            t = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/button')   # Find the blue button
            t.click()                # Click the button 
            time.sleep(2)           # Let the page load 
        
        except:
            pass
            html = driver.find_element(By.TAG_NAME,'html')
            html.send_keys(Keys.END)
            time.sleep(5)   # Let the page load
            block = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/ul')
            job_list = block.find_elements(By.CLASS_NAME, 'base-card')
            new = len(job_list)
            if new == current:
                break
            else:
                current = new

    links = []

    html = driver.find_element(By.TAG_NAME,'html')
    html.send_keys(Keys.END)
    block = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/ul')  # Find the block that includes the job list
    job_list = block.find_elements(By.CLASS_NAME, 'base-card')        # Find the job list section in the block
    print(len(job_list))                                              # Print the number of elements in the list  
    try:                                          # Protect the process in case null values exist
        for job in job_list:                    # Loop through the job list
            try:
                link = job.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')  # Extract the link
                links.append(link)                 # Append the link to the link list
            except:
                links.append(None)                 # If the link is not found, add null value to the list
                ValueError('no link')              # Error message     
    except:
        e = 'no path'
        ValueError(e)
        print(e)

    print(links)

    # contents = []            # Create an empty list to store data. 
    # for link in links:
    #     try:
    #         driver.get(link)   # Go to the link
    #         # Find the 'Show more' button and click it
    #         driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/button[1]').click()
    #         time.sleep(1)      # Let the details load
    #         try:
    #             content=driver.find_element(By.CLASS_NAME,'show-more-less-html__markup').text    # Find the details on page
    #             contents.append(content)       # Append the content into the list
    #         except:
    #             contents.append(None)
    #             ValueError('no content')    
    #     except:
    #         ValueError('smthng is wrong')
    #     time.sleep(5)

    dataframe= pd.DataFrame({'links':links,})
                                                         # Instantiate the Chrome browser
    # links = []                                                                           # Create an empty links list to use later as storage.
    # position_names = []                                                                  # Create an empty position names list to use later as storage.
    # companies = []                                                                       # Create an empty companies list to use later as storage.
    # locations = []  
    # i = 0
    # page_number = 2                                                                                # Base number that helps with arranging the iteration number
    # while i < page_number:                                                               # While loop that helps with scrolling. 
    #     html = driver.find_element(By.TAG_NAME,'html')                                   # Select anything on the page
    #     html.send_keys(Keys.END)                                                         # Send 'END' key to scroll down the page 
    #     i = i+1                                                                          # i increases incrementally. This helps with the number of repeats
    #     try:                                                                             # If the HTML does not include the desired element, the flow is protected with try func.
    #         t = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/button')# Find 'See more Jobs' button
    #         t.click()                                                                    # Click the button
    #         time.sleep(2)                                                                # Let the page load for 2 seconds.
    #     except:                                                                          # If a problem arises the flow continues. 
    #         pass
    #         time.sleep(3)                                                                # Wait for 3 secs
    #     block = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/ul')        # Find 
    #     job_list = block.find_elements(By.CLASS_NAME, 'base-card')
    #     try:
    #         for job in job_list:
    #             try:
    #                 link = job.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')
    #                 links.append(link)
    #             except:
    #                 links.append(None)
    #                 ValueError('no link')
    #             try:
    #                 position_name = job.find_element(By.TAG_NAME,'span').text
    #                 position_names.append(position_name)
    #             except:
    #                 position_names.append(None)
    #                 ValueError('no pos name')
    #             try:
    #                 company = job.find_element(By.CLASS_NAME,'hidden-nested-link').text
    #                 companies.append(company)
    #             except:
    #                 companies.append(None)
    #                 ValueError('no company')
    #             try:
    #                 location = job.find_element(By.CLASS_NAME,'job-search-card__location').text
    #                 locations.append(location)
    #             except:
    #                 locations.append(None)
    #                 ValueError('no location')
    #     except:
    #         e = 'no path'
    #         ValueError(e)
    #         print(e)
    #     data = pd.DataFrame({'Position':position_names,
    #             'Company':companies,
    #             'Location':locations,
    #             'Link':links})
    
    
    current_directory = Path(__file__).parents[0]
    output = current_directory.joinpath('output')
    
    if not os.path.exists(output):
        os.makedirs(output)
    
    today = datetime.now().strftime('%Y-%m-%d')

    file_name = output.joinpath(f'output_{today}.xlsx')

    dataframe.to_excel(file_name)
    print('DataFrame is written to Excel File successfully.')
   

    
    
    
    
            


    
    


    
        


        