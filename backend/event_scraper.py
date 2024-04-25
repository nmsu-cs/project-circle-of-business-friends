#
# Event scraper. 
# This code is set up for the version of crimsonconnection as of 4/17/2024. Significant updates to the page will likely break this functionality
#


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from time import sleep
import os

#Options for chrome UPDATE if you change the webdriver
chrome_options = Options()
chrome_options.add_argument('--headless') #Run in headless mode
chrome_options.add_argument('--disable-gpu') #Disable GPU acceleration


#The maximum amount of time (seconds) the scraper will wait for elements to load
WAIT_TIME = 3
MAX_RETRY = 3
RETRY_BREAK = 3 #Wait RETRY_BREAK seconds between retrying 

#Scrapes the home page for all events
#The scraper is meant to be used in a with block for proper resource management 
#i.e.
# with Scraper() as scraper:
#   [code using Scraper object]
class Home_Page_Scraper:
    def __init__(self, driver):
        # Launch a web browser (you need to have the appropriate driver installed, e.g., ChromeDriver)
        self.driver = driver
        events_url = "https://crimsonconnection.nmsu.edu/events"
        self.driver.get(events_url) 
        self.driver.implicitly_wait(WAIT_TIME)  ### !!!! Forces the program to wait up to 2 seconds for elements to load

    def get_hyperlinks(self):
        # Get all <a> tags on the MAIN page 
        all_a_tags = self.driver.find_elements(By.TAG_NAME, "a")
        

        event_links = list()
        for a_tag in all_a_tags:
            href = a_tag.get_attribute("href")
            event_links.append(href)
        
        return event_links[:len(event_links) - 2:] #Don't return last 2 links, they are non-events

#Scrapes an event page for date, description, location, and image
#The scraper is meant to be used in a with block for proper resource management 
#i.e.
# with Scraper() as scraper:
#   [code using Scraper object]
class Event_Scraper:
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url
        self.start_date = None
        self.end_date = None
        self.location = None
        self.desc = None
        self.title = None
        self.image = None
        self.host = None
        self.driver.get(self.url) 
        self.driver.implicitly_wait(WAIT_TIME)  ### !!!! Forces the program to wait up to 2 seconds for elements to load

    def populate_data(self):
        self.start_date, self.end_date = self.retry_get(self.get_dates)
        self.location = self.retry_get(self.get_location)
        self.desc = self.retry_get(self.get_desc)
        self.title = self.retry_get(self.get_title)
        # self.image = self.get_image()
        self.host = self.retry_get(self.get_host)

    def retry_get(self, getter):
        for _ in range(MAX_RETRY):
            try:
                return getter()
            except Exception as e:
                print(f"Error using {getter.__name__}:")
                print(f"Error occurred scraping URL {self.url}")
                print(e)
                sleep(RETRY_BREAK)
        raise RuntimeError(f"Failed to run {getter.__name__} after {MAX_RETRY} tries.")

    def get_dates(self):
        #The strategy here is to find the tag <strong>Date and Time</strong> on the HTML page, then get the next few <p> blocks that contain the actual date information. 
        date_time_element = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'Date and Time')]") #Find strong block with text Date and Time
        time_paragraphs = date_time_element.find_elements(By.XPATH, "./following-sibling::div/p")

        start_time = time_paragraphs[0].text
        start_time = start_time[:len(start_time) - len(" to"):]
        end_time = time_paragraphs[1].text
        return (start_time, end_time)

    
    def get_desc(self):
        desc_div = self.driver.find_element(By.XPATH, "//div[@class='DescriptionText']") #Find div with DescriptionText
        desc_text = desc_div.text

        return desc_text
    
    def get_title(self):
        # Find the div containing the title
        title_div = self.driver.find_element(By.XPATH, "//div[@style='display: inline-block; vertical-align: top; white-space: normal; padding-right: 90px;']")

        # Find the span element within the div
        span_element = title_div.find_element(By.TAG_NAME, "span")

        # Find the h1 element within the span
        h1_element = span_element.find_element(By.TAG_NAME, "h1")

        # Get the text from the h1 element
        title_text = h1_element.text
        
        return title_text
     
    def get_location(self):
        # Find <strong>Location</strong>
        location_element = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'Location')]")

        # Find all following <p> elements in the following <div>
        location_paragraphs = location_element.find_elements(By.XPATH, "./following-sibling::div/p")

        # Extract text content from each <p> element and concatenate
        location_text = ""
        for location_p in location_paragraphs:
            location_text += (location_p.text + "\n")

        # Print and return the concatenated text
        return location_text.strip()  # Strip leading and trailing whitespace

    
    def get_image(self):

        image_element = self.driver.find_element(By.XPATH, "(//div[@role='img'])[1]")

        #Screenshot the element
        image_element.screenshot('element_screenshot.png')

        #Read the image file binary
        with open('element_screenshot.png', 'rb') as file:
            image_data = file.read()

        #Remove the screenshot from system
        os.remove('element_screenshot.png')

        return image_data
   
    def get_host(self):
        host_element = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Host Organization')]") #Get h2 containing "Host Organizaion"
        host_name = host_element.find_element(By.XPATH, "./following::h3[1]") #Get the first h3 that follows
        return host_name.text.strip()

    def to_dict(self):
        out = dict()
        out["start_date"] = self.start_date
        out["end_date"] = self.end_date
        out["location"] = self.location
        out["desc"] = self.desc
        out['title']= self.title
        out["host"] = self.host
        out["url"] = self.url
        # out["image"] = self.image

        return out



"""
Only function that should be accessed externally

Returns a list of dictionaries that contain event information. 

"""
def generate_events():

    driver = webdriver.Chrome(options=chrome_options) 

    home_page_scraper =  Home_Page_Scraper(driver=driver)
    event_url_list = home_page_scraper.get_hyperlinks()
    
    event_list = list()
    for i in range(5):
        scraper = Event_Scraper(url=event_url_list[i], driver=driver)        
        scraper.populate_data()
        event_list.append(scraper.to_dict())
    
    driver.quit()

    return event_list