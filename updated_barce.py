from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("user-data-dir=selenium")
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--disable-dev-shm-usage')

url = "https://www.fotocasa.es/en" 
driver = webdriver.Chrome(executable_path = 'chromedriver.exe', options = options)  

driver.implicitly_wait(30)
driver.get(url) 

# driver.maximize_window()
driver.find_element_by_xpath('//*[@id="App"]/div[3]/div/div/div/footer/div/button[2]').click()  

#inputing barcelona in the input given on the webpage
try:
    input_field = driver.find_element_by_class_name('sui-AtomInput-input sui-AtomInput-input-size-m')   
except:    
    input_field = driver.find_element_by_xpath('//*[@id="App"]/div[1]/main/section/div[2]/div/div/div/div/div[2]/div[2]/form/div/div/div/div/div/input')
# first lets clear the text area incase if anything present in area 
# inp.clear()  
# folling command will type barcelona in text area selected.
input_field.send_keys('barcelona')

driver.find_element_by_xpath('//*[@id="App"]/div[1]/main/section/div[2]/div/div/div/div/div[2]/div[2]/form/button').click()

print(f"reached page {url}")   

# now extract the data from the page we reached on that website 
for i in range(0,25):
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    time.sleep(1)
for i in range(0,150):  
    ActionChains(driver).send_keys(Keys.UP).send_keys(Keys.UP).perform()
    
props = driver.find_elements_by_class_name('re-CardPackPremium-info')  
print(props)

with open('fotocasa.csv','w', encoding = 'utf-8') as f:
    wr = csv.writer(f, dialect = 'excel')
    wr.writerow(['Sr.No.','Type','Location', 'Price', 'Decription', 'Broker Name', 'Contact number', 'Link'])
    n = 0
    for prop in props:  
        n+=1
        # ActionChains(driver).send_keys(Keys.UP).perform()
        # time.sleep(3)
        num = n
        # //*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[7]/a
        name = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/div[1]/span/span[1]').text
        type = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/div[2]/a/h3/span[1]').text.split('in')[0] 
        loc = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/div[2]/a/h3/span[1]').text.split('in')[1] 
        price = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/div[2]/a/h3/span[2]/span[1]/span').text    #xpath('re-CardPrice')
        desc = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/div[2]/a/p/span').text
        contact = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/div[2]/div/div[1]/a/span/span[2]').text
        link = prop.find_element_by_xpath(f'//*[@id="App"]/div[2]/div[1]/main/div/div[2]/section/article[{n}]/a').get_attribute('href')
        # print(num, name, loc, price, contact) 
        wr.writerow([num, type, loc, price,desc, name, contact, link])
        # time.sleep(3)
    # ActionChains(driver).send_keys(Keys.UP).perform()

# Things to do:

# get the link for the mentioned properties   
# passing the authorizzation 
# description of the properties 
#     