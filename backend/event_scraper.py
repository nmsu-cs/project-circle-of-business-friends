#
# Event scraper. 
# This code is set up for the version of crimsonconnection as of 4/17/2024. Significant updates to the page will likely break this functionality
#



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import warnings
from time import sleep

#Options for chrome UPDATE if you change the webdriver
chrome_options = Options()
# chrome_options.add_argument('--headless') #Run in headless mode
# chrome_options.add_argument('--disable-gpu') #Disable GPU acceleration


# !!!Dependency!!!
# you MUST have this webdriver installed! 
WEB_DRIVER = webdriver.Chrome(options=chrome_options) 


#The maximum amount of time (seconds) the scraper will wait for elements to load
WAIT_TIME = 2

#Scrapes the home page for all events
#The scraper is meant to be used in a with block for proper resource management 
#i.e.
# with Scraper() as scraper:
#   [code using Scraper object]
class Home_Page_Scraper:
    def __init__(self):
        # Launch a web browser (you need to have the appropriate driver installed, e.g., ChromeDriver)
        self.driver = WEB_DRIVER

    def __enter__(self):
        # Load the webpage
        events_url = "https://crimsonconnection.nmsu.edu/events"
        self.driver.get(events_url) 
        self.driver.implicitly_wait(WAIT_TIME)  ### !!!! Forces the program to wait up to 2 seconds for elements to load
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
        print("SUCCESSFULLY EXITED\n\n")
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred exiting the web scraper: {exc_value} ")

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
    def __init__(self, url):
        self.driver = WEB_DRIVER
        self.url = url
        self.event = Event()

    def __enter__(self):
        self.driver.get(self.url) 
        self.driver.implicitly_wait(WAIT_TIME)  ### !!!! Forces the program to wait up to 2 seconds for elements to load
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred exiting the web scraper: {exc_value} ")


    def populate_event(self):
        self.event.start_date, self.event.end_date = self.get_dates()
        self.event.desc = self.get_desc()
        self.event.location = self.get_location()
        self.event.image = self.get_image()
        self.event.host = self.get_host()

    def get_dates(self):
        #The strategy here is to find the tag <strong>Date and Time</strong> on the HTML page, then get the next few <p> blocks that contain the actual date information. 
        date_time_element = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'Date and Time')]") #Find strong block with text Date and Time
        time_paragraphs = date_time_element.find_elements(By.XPATH, "./following-sibling::div/p")

        start_time = time_paragraphs[0].text
        start_time = start_time[:len(start_time) - len(" to"):]
        end_time = time_paragraphs[1].text
        return (start_time, end_time)

    
    def get_desc(self):
        desc_element = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Description')]") #Find h2 block with Description
        desc_paragraph = desc_element.find_element(By.XPATH, "./following-sibling::div[1]/p[1]") #Get the first <p> from the first following <div> 

        return desc_paragraph.text
    
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
        pass
   
    def get_host(self):
        host_element = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Host Organization')]") #Get h2 containing "Host Organizaion"
        host_name = host_element.find_element(By.XPATH, "./following::h3[1]") #Get the first h3 that follows
        print(host_name.text)
        return host_name.text.strip()
    

class Event:
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.location = None
        self.desc = None
        self.image = None
        self.host = None

    def to_dict(self):
        pass

    def to_json(self):
        pass
        


if __name__ == "__main__":
    #Testing code

    event_links = None
    try:
        # with Home_Page_Scraper() as scraper:
        #     event_links = scraper.get_hyperlinks()

        # print(f"Successfully pulled {len(event_links)} events. Now checking the first event:")
        # print(f"Attempting to open the following linK:\n{event_links[0]}")
        # sleep(2) #Evade rate limiting

        with Event_Scraper("https://crimsonconnection.nmsu.edu/event/9708885") as scraper:
            # scraper.get_dates()
            # scraper.get_location()
            # scraper.get_desc()
            scraper.get_host()
    except Exception as e:
        print(f"An exception has occurred: {e}")


        




