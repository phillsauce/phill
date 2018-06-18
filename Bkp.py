from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random
from CodeWarrior.Standard_Suite import windows
#import org.openqa.selenium.support.ui.ExpectedConditions; 
#import org.openqa.selenium.support.ui.WebDriverWait; 
  
#This function shows what the count of test this is
def get_var_value(filename="count_file.txt"):
    with open(filename, "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        f.close()
        return val
    
test_count = get_var_value()
print("This script has been run {} times.".format(test_count))

platforms = ['Windows 10', 'Windows 8.1', 'Windows 7', 'macOS 10.13', 'macOS 10.12', 'Linux']
windows_browserName = ['chrome', 'firefox']
sauce_version = ['48.0']



#Select the platform from the list above
sauce_platform = random.choice(platforms)

#Based on the platform you randomly choose a browser
if "Windows" in sauce_platform:
    sauce_browserName = random.choice(windows_browserName)
else:
    sauce_browserName = 'chrome'
    
#Based on the browser you randomly choose a version
if "chrome" in sauce_browserName:
    sauce_version = random.randint(29,67)
else:
    sauce_version = 'latest'
    
#Now this is the function. We're going to theuselessweb.com,
#clicking the button, then checking if the title has even or odd amount of characters.
#If even it's a pass test, if odd it's a failure.

sauceParameters = {
    'name': "Python - Random Test: " + str(test_count),
    'platform': str(sauce_platform),
    'browserName': str(sauce_browserName),
    'version': str(sauce_version),
    'tags':['Python'],
    'customData':{'Test Number':str(test_count)}, 
#    'browserName': "chrome",
#    'version': "67.0",
#    'platform': 'Windows 10',
#    'extendedDebugging':'true',
    }

print(sauceParameters.items())

#Connect to sauce
driver = webdriver.Remote(
   command_executor='http://phillipramirez:8d1823e8-289b-4737-b678-87e93623ca94@ondemand.saucelabs.com:80/wd/hub',
   desired_capabilities=sauceParameters)
  
#driver.get("https://saucelabs.com/test/guinea-pig") # Navigate to webpage
#if not "Google" in driver.title:
#    raise Exception("Unable to load google page!")
#    driver = webdriver.Remote(desired_capabilities={'passed':'false'})  
#time.sleep(20)

#elem = driver.find_element_by_partial_link_text('i am a ')
#print driver.title # Ensure you're on the guinea pig new page
#elem.click()

driver.get("http://www.theuselessweb.com/") #Navigate to Useless web
#driver.get('https://www.discuvver.com/') #Navigate to random site generator
print driver.title # Ensure on Useless Web

elem = driver.find_element_by_id('button') #Find the button
#elem = driver.find_element_by_class_name('btn btn\-default btn\-random')
#elem = driver.find_element_by_css_selector('.btn.btn-default.btn-random')
#time.sleep(20)
elem.click()

#elem = driver.find_element_by_id("fieldName")
#elem.send_keys('Zimbo Zambo') #Add a random name
#time.sleep(20)
#elem = driver.find_element_by_id("fieldEmail")
#elem.send_keys('test@email.net') #Add a random email
time.sleep(10)
#elem.submit()
print('this is the page at the end: ' + driver.title)
print('current window handle this is the page at the end: ' + driver.current_window_handle)
print('current url this is the page at the end: ' + driver.current_url)
#WebDriverWait wait = new WebDriverWait(driver, 10); 
#WebElement messageElement = wait.until( ExpectedConditions.presenceOfElementLocated(By.id("fieldName")) );

driver.quit() #Done with test