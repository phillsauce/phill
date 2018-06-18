'''
Imports used for these functions
'''
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import time
import random
#from CodeWarrior.Standard_Suite import windows
import os
#import multiprocessing
#from StdSuites.Standard_Suite import starts_with


'''
This function gets the count of the test
from a file and returns the value
'''
def get_var_value():
    with open('count_file.txt', "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        f.close()
        return val


'''
This function connects to Sauce Labs
and creates a session
test_count is to add an int to the title/tag
random_enabled is to turn on or off random platform selection
random_enabled == 1 is for random, anything else is hard-coded
'''
def connect_to_sauce(test_count, random_enabled):
    if random_enabled == 1:
        random_tag = 'Random'
        #To randomly choose what platform you'd want to test on
        platforms = ['Windows 10', 'Windows 8.1', 'Windows 7', 'macOS 10.13', 'macOS 10.12', 'Linux']
        windows_browserName = ['chrome', 'firefox', 'internet explorer']
        mac_browserName = ['chrome', 'firefox']
        linux_browserName = ['chrome', 'firefox']
        sauce_version = ['48.0']
        #Select the platform from the list above
        sauce_platform = random.choice(platforms)
    
        #Based on the platform you randomly choose a browser
        if sauce_platform.startswith('Windows'):
            sauce_browserName = random.choice(windows_browserName)
        elif sauce_platform.startswith('macOS'):
            sauce_browserName = random.choice(mac_browserName)
        elif "Linux" in sauce_platform:
            sauce_browserName = random.choice(linux_browserName)
            
        #Based on the browser you randomly choose a version
        if 'chrome' in sauce_browserName and 'Windows' in sauce_platform:
            sauce_version = random.randint(32,67)
        elif 'chrome' in sauce_browserName and 'macOS' in sauce_platform:
            sauce_version = random.randint(34,67)
        elif 'chrome' in sauce_browserName and 'Linux' in sauce_platform:
            sauce_version = random.randint(41,48)
        elif 'firefox' in sauce_browserName and 'Windows' in sauce_platform:
            sauce_version = random.randint(15,60)
        elif 'firefox' in sauce_browserName and 'macOS' in sauce_platform:
            sauce_version = random.randint(32,67)
        elif 'firefox' in sauce_browserName and 'Linux' in sauce_platform:
            sauce_version = random.randint(38,45)
        elif 'internet explorer' in sauce_browserName:
            sauce_version = random.randint(8,11)        
        else:
            sauce_version = 'latest'
            
    #If the randomness is not chosen, then use defaults below
    else:
        random_tag = 'Not Random'
        sauce_platform = 'Windows 10'
        sauce_browserName = 'chrome'
        sauce_version = 'latest'

    #Use the parameters generated randomly above and connect
    #to the SauceLabs account    
    sauceParameters = {
        'name': 'Unit Testing: ' + str(test_count),
        'tags':['Python', 'Unit Testing', random_tag],
        'customData':{'Test Number':str(test_count)}, 
        'platform': str(sauce_platform),
        'browserName': str(sauce_browserName),
        'version': str(sauce_version),
        'extendedDebugging':'true',
        'build':'Python Randomness',
        #Adding in pre-run conditions
        'prerun':{ # This prerun starts the installation for the Nexon launcher, but doesn't complete install.
            'executable': 'http://download.nxfs.nexon.com/download-launcher?file=NexonLauncherSetup.exe',
            'args': '',
            'background': 'true',
            }
        }
    #print('given parameters: ->' + str(sauceParameters.items()) + '<-')
    
    #Connect to sauce
    driver = webdriver.Remote(
       command_executor='http://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.saucelabs.com:80/wd/hub',
       desired_capabilities=sauceParameters)
    return driver


def run_sauce_test(driver):
    #Now this is the function. We're going to theuselessweb.com,
    #clicking the button, then returning the new tab's title    
    driver.get("http://www.theuselessweb.com/") #Navigate to Useless web
    elem = driver.find_element_by_id('button') #Find the button
    elem.click() # Click the button
    #Change to the other (2nd) tab
    driver.switch_to_window(driver.window_handles[1])
    return driver.title

