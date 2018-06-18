from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random
from CodeWarrior.Standard_Suite import windows
import os
import multiprocessing
  
#This function shows what the count of test this is
def get_var_value(filename="count_file.txt"):
    with open(filename, "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        f.close()
        return val
    
#print("This script has been run {} times.".format(test_count))

#To randomly choose what platform you'd want to test on
platforms = ['Windows 10', 'Windows 8.1', 'Windows 7', 'macOS 10.13', 'macOS 10.12', 'Linux']
windows_browserName = ['chrome', 'firefox']
sauce_version = ['48.0']


def run_sauce_test():
    #Increment the test counter
    test_count = get_var_value()
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
    #    'name': "Python - Random Test: " + str(test_count),
    #    'platform': str(sauce_platform),
    #    'browserName': str(sauce_browserName),
    #    'version': str(sauce_version),
        'name': 'Pass or Fails Testing',
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest',
        'tags':['Python'],
        'customData':{'Test Number':str(test_count)}, 
        'extendedDebugging':'true',
        'build':'Python testing - repeats',
        #Adding in pre-run conditions
        'prerun':{ # This prerun starts the installation for the Nexon launcher, but doesn't complete install.
            'executable': 'http://download.nxfs.nexon.com/download-launcher?file=NexonLauncherSetup.exe',
            'args': '',
            'background': 'true',
            }
        }
    
    #print(sauceParameters.items())
    
    #Connect to sauce
    driver = webdriver.Remote(
       command_executor='http://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.saucelabs.com:80/wd/hub',
       desired_capabilities=sauceParameters)
    
    driver.get("http://www.theuselessweb.com/") #Navigate to Useless web
    #print ('Starting title is: ; ' + str(driver.title)) # Ensure on Useless Web
    
    #driver.execute_script('sauce:intercept', {
    #    "url": "*",
    #    "redirect": "https://google.com"
    #})
    
    #'sauce: break'
    elem = driver.find_element_by_id('button') #Find the button
    elem.click()
    #driver.execute_script('sauce: break')
    
    #Change to the other tab
    driver.switch_to_window(driver.window_handles[1])
    
    
    #If the new tab's title is an even amount of characters, pass
    #Otherwise, fail the test
    if len(driver.title) % 2 == 0:
        driver.execute_script('sauce: job-result=passed')
    #    print 'test passed'
    else:
        driver.execute_script('sauce: job-result=failed')
    #    print 'test failed'
    
    driver.get("https://www.google.com/") #Navigate to Google on new tab
    
    time.sleep(15)
    
    driver.quit() #Done with test
    


#This is actually where the script is executed from below.
#This uses the multithreading to execute run_sauce_test multiple times

if __name__ == '__main__':
    jobs = [] #Array for the jobs
#    for i in range(random.randint(0,10)): # Run X times. Currently 20. Integer.
    for i in range(20): # Run X times. Integer.
        p = multiprocessing.Process(target=run_sauce_test) #Define what function to run multiple times.
        jobs.append(p) # Add to the array.
        p.start() #Start the functions.
        print('this is the run for: '+ str(i))



