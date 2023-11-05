from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

class FullSet(set):
    def __contains__(self, item):
        return True

month_to_number = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


def click_button_by_id(driver, id, delay=0.3):
    button_xpath = "//*[@id='"+id+"']" 
    button = driver.find_element(By.XPATH, button_xpath)
    button.click()
    #time.sleep(delay)

def click_button_by_class_and_ancestor_class(driver, element_class, ancestor_class, delay=0):
    button_xpath = f"//*[@class='{ancestor_class}']//*[@class='{element_class}']"


    button = driver.find_element(By.XPATH, button_xpath)
    button.click()
    #time.sleep(delay)

def click_button_by_class_and_2ancestor_class_and_desired_text(driver, element_class1, element_class2, ancestor_class, desired_text, delay=0):
    button_xpath = f"//*[@class='{ancestor_class}']//*[text()='{desired_text}' and (@class='{element_class1}' or @class='{element_class2}')]"

    button = driver.find_element(By.XPATH, button_xpath)
    button.click()
    #time.sleep(delay)



def get_choice_math_and_year(driver):
    # Locate the element with the month and year
    element_xpath = "//*[@class='datepicker-switch']"
    date_element = driver.find_element(By.XPATH, element_xpath)

    # Extract and split the month and year
    month_year = date_element.text
    month, year = month_year.split()
    year=int(year)
    month = month_to_number[month]
    return month, year
    

def set_date(driver, date, id):

    # Click the "id" button
    click_button_by_id(driver, id)

    month, year = get_choice_math_and_year(driver)
    
    while year>date[2] or (year==date[2] and month>date[1]):
        click_button_by_class_and_ancestor_class(driver, "prev", " table-condensed")
        month, year = get_choice_math_and_year(driver)
    
    click_button_by_class_and_2ancestor_class_and_desired_text(driver, "day", "today day", " table-condensed", str(date[0]))
    time.sleep(1)
def set_dates(driver, date_from, date_to):
    # Click the "Choose Dates" buttons
    click_button_by_id(driver, "ah-chooseDates")

    set_date(driver, date_from, "txtDateFrom")
    set_date(driver, date_to, "txtDateTo")

def fetch_alerts(driver, locations_set, category_set):
    # Scroll down to trigger the loading of more content
    pressed_show_more = 0
    try:
        while True:
            show_more = driver.find_elements(By.XPATH, "//*[contains(@class, 'alertShowMore')]")[pressed_show_more]
            driver.execute_script("arguments[0].scrollIntoView({ block: 'center' });", show_more)
            time.sleep(0.1)
            show_more = driver.find_elements(By.XPATH, "//*[contains(@class, 'alertShowMore')]//span")[pressed_show_more]
            pressed_show_more+=1
            #print("trying to click...")
            show_more.click()
            time.sleep(0.1)
            #print("clicked")
            
    except Exception as e:
        pass
    
    alerts = driver.find_elements(By.XPATH, "//*[contains(@class, 'alertTableCategory') or contains(@class, 'alertDetails') or contains(@class, 'alertTableDate')]")

    json_array = []

    for alert in alerts:
        class_attribute = alert.get_attribute("class")
        if 'alertTableCategory' in class_attribute:
            alert_category = alert.text
        elif 'alertDetails' in class_attribute:
            alert_time, alert_locations = alert.text.splitlines()
            alert_locations = alert_locations.split(", ")
            for alert_location in alert_locations:
                if alert_location in locations_set and alert_category in category_set:
                    json_element = {
                        "date" : alert_date,
                        "time" : alert_time,
                        "location" : alert_location,
                        "category" : alert_category
                    }
                    #print(json_element)
                    json_array.append(json_element)
                
        elif 'alertTableDate' in class_attribute:
            if alert.text!="":
                _, alert_date = alert.text.split()
    return json_array



def get_alerts_json(date_from, date_to, locations_set=FullSet(), category_set=FullSet()):
    # Initialize a web driver (you need to have a compatible web driver installed, like ChromeDriver)
    driver = webdriver.Chrome()  # You can use other browsers by specifying their drivers (e.g., Firefox, Edge, etc.)

    # Open the webpage
    url = "https://www.oref.org.il/12481-en/Pakar.aspx"
    driver.get(url)

    time.sleep(0.3)

    set_dates(driver, date_from, date_to)

    json_array = fetch_alerts(driver, locations_set, category_set)

    # Close the web driver
    driver.quit()

    return json_array


def parse_date(date_string, deli):
    day, month, year = date_string.split(deli)
    return (int(day), int(month), int(year))

if __name__=="__main__":
    if len(sys.argv)<3:
        print("Usage: python3 DD-MM-YYYY DD-MM-YYYY")
        sys.exit(1)
    
    print(get_alerts_json(parse_date(sys.argv[1], "-"), parse_date(sys.argv[2], "-")))