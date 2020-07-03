username = '###'
pw = '###'
needToSignIn = False # Only needs to be True if cookies are expired i.e. you haven't logged in in a while
                     # Alternatively you can log in manually through the Chrome popup
url = 'https://be.my.ucla.edu/ClassPlanner/ClassPlan.aspx'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from playsound import playsound
import time

DRIVER_PATH = 'C:/path/to/chromedriver' # You need to download the appropriate version of chromedriver
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=C:\\path\\to\\Google\\Chrome\\User Data') # Path to your Chrome user profile. Alternatively enter any path and a new profile should be created

driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
driver.get(url)

if needToSignIn:
    username_field = driver.find_element_by_name('j_username')
    password_field = driver.find_element_by_name('j_password')
    signInButton = driver.find_element_by_name('_eventId_proceed')

    # Comment these out if your username and/or password is autosaved in Chrome
    username_field.send_keys(username)
    password_field.send_keys(pw)
    
    signInButton.click()

time.sleep(2) # give time for authentication

closedClasses = []

while True:
    driver.get(url)
    for i in range(20):
        print(' ')
    
    closedCount = []
    tables = driver.find_elements_by_css_selector('tbody.courseItem')
    
    for table in tables: # Get class data
        print('--------------------------------------------')
        className = table.find_element_by_css_selector('td.SubjectAreaName_ClassName p:nth-child(2)')
        print(className.text)
        cell = table.find_element_by_css_selector('table.coursetable tbody:nth-child(2) tr:nth-child(1) td:nth-child(3)')
        print(cell.text)
        if (cell.text[0] == 'C'):
            closedCount.extend([className.text])
    
    if (len(closedCount) < len(closedClasses)): # Check to see if anything's changed since the previous iteration
        #playsound('C:/path/to/soundeffect.mp3') # Optional sound effect
        print('Class open')
        ct = 0
        try:
            while (closedCount[ct] == closedClasses[ct]):
                ct+=1
            print(closedClasses[ct])
        except:
            print(closedClasses[-1])
    closedClasses = closedCount;
    
    
    print('============================================')
    print(str(len(closedClasses)) + ' closed class(es): ')
    for eachClass in closedClasses:
        print(eachClass)
    time.sleep(15) # seconds, change if you want but UCLA might get pissy if it's too high