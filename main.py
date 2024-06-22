import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

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
        email_field = driver.find_element(by=By.ID, value="username")
        password_field = driver.find_element(by=By.ID, value="password")

        email_field.send_keys(account_email)
        password_field.send_keys(account_password)
        password_field.send_keys(Keys.ENTER)
        print("CAPTCHA - Solve Puzzle Manually")
        input("Press Enter when you have solved the Captcha")

        time.sleep(5)
        
        apply_button = driver.find_element(by=By.LINK_TEXT, value="Jobs")
        apply_button.click()
        
        number = 100
        while True:

            # xpath = f'//*[@id="jobs-search-box-keyword-id-ember{number}"]'
            id_job = f"jobs-search-box-keyword-id-ember{number}"
            id_loc = f"jobs-search-box-location-id-ember{number}"
            try:
                job_title_field = driver.find_element(by=By.ID, value=id_job)
                job_location_field = driver.find_element(by=By.ID, value=id_loc)
                job_title_field.send_keys("Design Graphique / Directeur Artisitique")
                job_location_field.send_keys("Paris Toronto")
                job_title_field.send_keys(Keys.ENTER)
            except:
                number+=1
                continue
            else:
                print(f"Job Title and Location Entered number:{number}")
                break

        # job_title_field = driver.find_element(by=By.XPATH, value='//*[@id="jobs-search-box-keyword-id-ember326"]')
        # job_title_field.send_keys("Design Graphique")
        # job_title_field.send_keys(Keys.ENTER)
        
        # "Search by title, skill, or company"
        # for listing in all_listings:
        #     print("Opening Listing")
        #     listing.click()
        #     time.sleep(2)
        #     try:
        #         # Click Apply Button
        #         apply_button = self.driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
        #         apply_button.click()

        #         # Insert Phone Number
        #         # Find an <input> element where the id contains phoneNumber
        #         time.sleep(5)
        #         phone = self.driver.find_element(by=By.CSS_SELECTOR, value="input[id*=phoneNumber]")
        #         if phone.text == "":
        #             phone.send_keys(phone_number)

        #         # Check the Submit Button
        #         submit_button = self.driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        #         if submit_button.get_attribute("data-control-name") == "continue_unify":
        #             abortApplication()
        #             print("Complex application, skipped.")
        #             continue
        #         else:
        #             # Click Submit Button
        #             print("Submitting job application")
        #             submit_button.click()

        #         time.sleep(2)
        #         # Click Close Button
        #         close_button = self.driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        #         close_button.click()

        #     except NoSuchElementException:
        #         abortApplication()
        #         print("No application button, skipped.")
        #         continue

        return
                
if __name__ == "__main__":
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
    applicationFilling()
    # killer()

    
    
    
    
            


    
    


    
        


        