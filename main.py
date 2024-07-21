import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
from datetime import datetime


class LectureLang:
    def __init__(self, driver):
        self._driver = driver
        self.lang = self.driver.find_element(By.XPATH, "//html").get_attribute('lang')

    @property
    def driver(self):
        return self._driver

    def __call__(self):
        if self.lang == "fr":
            ID = "S’identifier"
            JOB = "Offres d’emploi"
        else:
            ID = "Sign in"
            JOB = "Jobs"
        return [ID, JOB] 


        
class LinkedInUrl:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("URL_LINKEDIN")
    
    def __call__(self):
        return self.url
    
class SetupDriver:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--start-maximized")
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
        try:
            reject_button = self.driver.find_element(by=By.CSS_SELECTOR, value='button[action-type="DENY"]')
            reject_button.click()
        except:
            print("No Cookies to Deny")
        return
    
class SignIn:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver
    
    def __call__(self, ID):
        time.sleep(2)
        sign_in_button = self.driver.find_element(by=By.LINK_TEXT, value= ID )
        sign_in_button.click()
        return
    
class JobListing:

    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    def __call__(self):
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[1]/div/ul')
        # job_list = block.find_elements(By.CLASS_NAME, 'base-card')
        # job_list = block.find_elements(By.CLASS_NAME, 'ember-view')
        return
    
class GoToEndWebPage:

    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    def __call__(self):
        html = self.driver.find_element(By.TAG_NAME,'html')
        html.send_keys(Keys.END)
        time.sleep(5)
        return
    

class SeekButtonAndClick:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver
    
    def __call__(self):
        
        button = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/button')
        button.click()
        time.sleep(2)
        return

class CredentialsInput:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver

    def __call__(self):
        time.sleep(5)
        env_vars = EnvLoader()
        account_email, account_password, _ = env_vars()
        email_field = self.driver.find_element(by=By.ID, value="username")
        password_field = self.driver.find_element(by=By.ID, value="password")

        email_field.send_keys(account_email)
        password_field.send_keys(account_password)
        password_field.send_keys(Keys.ENTER)
        print("CAPTCHA - Solve Puzzle Manually")
        input("Press Enter when you have solved the Captcha")

        time.sleep(5)

        

class ApplicationFilling:
    def __init__(self, driver):
        self._driver = driver
    
    @property
    def driver(self):
        return self._driver

    def __call__(self, JOB):
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
        
        apply_button = driver.find_element(by=By.LINK_TEXT, value=JOB)
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
        
        # job_listing = self.driver.find_element(by=By.CLASS_NAME, value="scaffold-layout__list-container")
        return

def chunk_1():
    linkedin_url = LinkedInUrl()
    url = linkedin_url()
    mySetup = SetupDriver()
    driver = mySetup.driver

  
    cookiesdenial = CookiesDenial(driver)
    signIn = SignIn(driver)
    applicationFilling = ApplicationFilling(driver)
    #killer = KillSession(driver)
    navigate = NavigateUrl(driver, url)

    navigate()
    lect_language = LectureLang(driver)
    [ID, JOB] = lect_language()
    cookiesdenial()
    signIn(ID)
    applicationFilling(JOB)
    #killer()


def chunk_2():
    path = f'https://www.linkedin.com/jobs/search?keywords=Design%20Graphique&location=Paris&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    mySetup = SetupDriver()
    driver = mySetup.driver
                
# if __name__ == "__main__":
#     print("working in progress dude")

#     linkedin_url = LinkedInUrl()
#     url = linkedin_url()
#     mySetup = SetupDriver()
#     driver = mySetup.driver
    
#     cookiesdenial = CookiesDenial(driver)
#     signIn = SignIn(driver)
#     my_job_listing = JobListing(driver)
#     move_to_end = GoToEndWebPage(driver)
#     look_for_button = SeekButtonAndClick(driver)
#     applicationFilling = ApplicationFilling(driver)
#     killer = KillSession(driver)
#     navigate = NavigateUrl(driver, url)

#     navigate()
#     cookiesdenial()
#     signIn()
   
#     applicationFilling()
    
#     time.sleep(5)
#     current_list = my_job_listing()
#     current_size = len(current_list)
#     move_to_end()
#     driver.execute_script("scrollBy(0,-500);")

#     # prev_height = -1
#     # scroll_count = 0
#     # max_scrolls = 10
#     # while scroll_count < max_scrolls:
#     #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     #     time.sleep(1)  # give some time for new results to load
#     #     new_height = driver.execute_script("return document.body.scrollHeight")
#     #     if new_height == prev_height:
#     #         break
#     #     prev_height = new_height
#     #     scroll_count += 1

#     while True:
#         move_to_end()
#         driver.execute_script("scrollBy(0,-500);")
#         try:
#             look_for_button()
        
#         except:
#             move_to_end()
#             current_list = my_job_listing()
#             new_size = len(current_list)
#             if new_size == current_size:
#                 break
#             else:
#                 current_size = new_size

#     move_to_end()
#     job_list = my_job_listing()
#     print(f"finally we have: {len(job_list)} in this displayed webpage")
#     links = []
#     contents = []
#     position_names = []
#     companies = []
#     locations = []

#     try:                                          
#         for job in job_list:
#             try:
#                 link = job.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')  # Extract the link
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

#     for link in links:
#         try:
#             temp_nav = NavigateUrl(driver, link)
#             temp_nav()
#             driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/button[1]').click()
#             time.sleep(1)
#             try:
#                 content=driver.find_element(By.CLASS_NAME,'show-more-less-html__markup').text
#                 contents.append(content)
#             except:
#                 contents.append(None)
#                 ValueError('no content')    
#         except:
#             contents.append(None)
#             ValueError('smthng is wrong')           


#     dataframe = pd.DataFrame({'contents': contents,
#                              'links':links,
#                              'Position':position_names,
#                              'Company':companies,
#                              'Location':locations})
                                                      
#     current_directory = Path(__file__).parents[0]
#     output = current_directory.joinpath('output')
    
#     if not os.path.exists(output):
#         os.makedirs(output)
    
#     today = datetime.now().strftime('%Y-%m-%d')

#     file_name = output.joinpath(f'output_{today}.xlsx')

#     dataframe.to_excel(file_name)
#     print('DataFrame is written to Excel File successfully.')
#     killer()

# ======= No Login =========
# if __name__ == "__main__":
#     url = f'https://www.linkedin.com/jobs/search?keywords=Design%20Graphique&location=Paris&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
#     mySetup = SetupDriver()
#     driver = mySetup.driver

#     cookiesdenial = CookiesDenial(driver)
#     signIn = SignIn(driver)
#     applicationFilling = ApplicationFilling(driver)
#     killer = KillSession(driver)
#     navigate = NavigateUrl(driver, url)

#     my_job_listing = JobListing(driver)

#     navigate()
#     cookiesdenial()
#     job_list = my_job_listing()
# ======= No Login =========

class MyJobQuery:
    def __init__(self, query, location):
        self._query = query
        self._location = location
        self._page_num = 1
        self._limit = 1
    
    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def page_num(self):
        return self._page_num

    @page_num.setter
    def page_num(self, value):
        self._page_num = value

    @property
    def limit(self):
        return self._limit
    
    @limit.setter
    def limit(self, value):
        self._limit = value

    def __call__(self):
        job_url = f'https://www.linkedin.com/jobs/search/?keywords={self.query}&location={self.location}&start={25 * (self.page_num - 1)}'
        return job_url
    


if __name__ == "__main__":
    print("working in progress dude")

    linkedin_url = LinkedInUrl()
    url = linkedin_url()
    mySetup = SetupDriver()
    driver = mySetup.driver
    
    cookiesdenial = CookiesDenial(driver)
    signIn = SignIn(driver)
    
    my_job_listing = JobListing(driver)
    move_to_end = GoToEndWebPage(driver)
    look_for_button = SeekButtonAndClick(driver)
    applicationFilling = ApplicationFilling(driver)
    
    my_credentials = CredentialsInput(driver)
    killer = KillSession(driver)
    navigate = NavigateUrl(driver, url)

    navigate()
    cookiesdenial()
    signIn()

    my_credentials()

    query ="Design Graphique / Directeur Artisitique"
    location = "Paris"

    my_job_query = MyJobQuery(query, location)


# =======to save================
    # while True:

    #     temp_url = my_job_query()
    #     navigate = NavigateUrl(driver, temp_url)
    #     navigate()

    #     try:
    #         my_job_listing()
    #         my_job_query.page_num+=1
    #     except:
    #         print(f"No more pages - max page is {my_job_query.page_num-1}")
    #         my_job_query.limit = my_job_query.page_num-1
    #         break
    #     else:
    #         print(f"All good - page {my_job_query.page_num-1}")
    #         continue
# ==============================

    links = []
    all_details = []
    position_names = []
    companies = []
    locations = []
    my_job_query.page_num = 1
    url_job_listing = my_job_query()
    navigate = NavigateUrl(driver, url_job_listing)
    navigate()

    list_items = driver.find_elements(By.CLASS_NAME,"occludable-update")
    for i,job in enumerate(list_items):
        time.sleep(2)
        t = 0
        while True:
            try:
                ActionChains(driver).scroll_to_element(job).perform()
                print("action done!")
                driver.execute_script("arguments[0].scrollIntoView(true);", job)
                print('scroll done!')
            except:
                t+=1
                if t == 100:
                    break
                print("Nothing found yet")
                continue
            else:
                print(f"Found it after {t} times")
                break

        time.sleep(1)
        job.click()
        time.sleep(1)
        
        try:
            link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')  # Extract the link
            link = job.find_element(By.CLASS_NAME, 'job-card-container__link').get_attribute('href')  # Extract the link
            links.append(link)
            print(link)
        except:
            links.append(None)
            ValueError('no link')
        
        try:
            position, company, location = job.text.split('\n')[1:4]
            position_names.append(position)
            companies.append(company)
            locations.append(location)
        except:
            position_names.append(None)
            companies.append(None)
            locations.append(None)
            ValueError('no pos name')
        
        try:
            details = driver.find_element(By.ID,"job-details").text
            all_details.append(details)
        except:
            all_details.append(None)
            ValueError('no details')
    
    dataframe = pd.DataFrame({'links':links,
                             'Position':position_names,
                             'Company':companies,
                             'Location':locations,
                             'Details':all_details})
                                                      
    current_directory = Path(__file__).parents[0]
    output = current_directory.joinpath('output')
    
    if not os.path.exists(output):
        os.makedirs(output)
    
    today = datetime.now().strftime('%Y-%m-%d')

    file_name = output.joinpath(f'output_{today}.xlsx')

    dataframe.to_excel(file_name)
    print('DataFrame is written to Excel File successfully.')
    killer()
    
    
    
            


    
    


    
        


        