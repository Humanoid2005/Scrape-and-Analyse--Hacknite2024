import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_new_url(url,header_line):
    options = ChromeOptions()
    path = './chromedriver.exe'
    options.headless = True
    ser = Service(path)
    driver = webdriver.Chrome(service=ser, options=options)
    driver.get(url)

    wait = WebDriverWait(driver,10)
    h2_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//h2[@class='mb-srp__card--title'][@title='{header_line}']")))

    actions = ActionChains(driver)
    actions.move_to_element(h2_element).click().perform()

    window_before = driver.current_window_handle
    windows_after = driver.window_handles

    if(len(windows_after)==2):
        if(windows_after[0]==window_before):
            new_window = windows_after[1]
        else:
            new_window = windows_after[0]
        driver.switch_to.window(new_window)

    new_url = driver.current_url
    driver.quit()
    return new_url

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    houses = soup.find_all("div",class_ = "mb-srp__card__container")

    house_list = []
    
    for i in houses:
        details = {}
        x = i.find("div",class_ = "mb-srp__card__info")
        info1 = x.h2.text.split()
        header_line = x.h2['title']
        try:
            link = get_new_url(url,header_line)
            details['Link'] = link
            print(header_line)
        except Exception as e:
            details['Link'] = url
        
        if(details.get('Link',url)==url):
            print(header_line)
            details['Link'] = url

        #Getting the location
        location  = ""
        idx = info1.index("in")
        idx = idx+1
        while(info1[idx]!='Bangalore'):
            location = location + info1[idx] + " "
            idx = idx + 1
        location = location.strip()
        location = location.rstrip(',')
        details['Location']= location

        
        #info1[1] is BHK
        details[info1[1]] = int(info1[0].strip())
        

        #Getting builder details and additional details
        builderinfo1 = i.find("div",class_ = "mb-srp__card__developer")
        if(builderinfo1==None):
            builderinfo2 = i.find("div",class_ = "mb-srp__card__society")
            builder_link = builderinfo2.a['href']
            builder = builderinfo2.a.text
            details['Builder'] = builder
            details['BuilderLink'] = builder_link
        else:
            builder = builderinfo1.a.span.text
            builder_link = builderinfo1.a['href']
            details['Builder'] = builder
            details['BuilderLink'] = builder_link

        #further details
        Summary = i.find("div",class_ = "mb-srp__card__summary__list")
        points = Summary.find_all("div",{'class':'mb-srp__card__summary__list--item'})
        for i in points:
            info2 = i.find_all("div")
            if(info2[0].text == 'Super Area'):
                details[info2[0].text+' (in sqft)'] = int(info2[1].text.split()[0])
            elif(info2[0].text == 'Status'):
                details['Status'] = info2[1].text
            elif(info2[0].text == 'Under Construction'):
                details['Status'] = 'Under Construction '+info2[1].text
            elif(info2[0].text == 'Bathroom' or info2[0].text == 'Balcony'):
                details[info2[0].text] = int(info2[1].text.strip())
            elif(info2[0].text == 'Car Parking'):
                details[info2[0].text] = int(info2[1].text[0].strip())
            else:
                details[info2[0].text] = info2[1].text
                
            
            
        
        if(details.get('Status','Under Construction')=='Under Construction'):
            details['Status'] = 'Under Construction'
        if(details.get('Balcony',0) == 0):
            details['Balcony'] = 0
        if(details.get('Car Parking',0)==0):
            details['Car Parking'] = 0
        
        house_list.append(details)
        

    prices = soup.find_all("div",class_ = 'mb-srp__card__estimate')

    idx = 0
    for i in range(len(prices)):
        costs  = prices[i].find("div",class_ = 'mb-srp__card__price')
        cost = costs.find_all("div")
        
        tcosttext = cost[0].text
        tcost = float(tcosttext.split()[0][1:])
        if(tcosttext.split()[1]=='Cr'):
            tcost = tcost*10000000
        elif(tcosttext.split()[1]=='Lac'):
            tcost = tcost*100000

        if(len(cost)>1):    
            percosttext = cost[1].text
            raw = percosttext.split()[0]
            costper = ''
            for i in raw:
                if(i.isdigit()):
                    costper += i
            costpersqft = int(costper)
            house_list[idx]['CostPerSqft'] = costpersqft
        else:
            if(house_list[idx].get('Super Area (in sqft)','Not Known')!='Not Known'):
                house_list[idx]['CostPerSqft'] = house_list[idx]['TotalCost']/house_list[idx]['Super Area (in sqft)']
            else:
                house_list[idx]['CostPerSqft'] = -1
                
            
        
        house_list[idx]['TotalCost'] = int(tcost)
        if(house_list[idx].get('Super Area (in sqft)','Not Known')=='Not Known'):
            house_list[idx]['Super Area (in sqft)'] = house_list[idx]['TotalCost']/house_list[idx]['CostPerSqft']
        idx = idx + 1
        
    return house_list

url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore"
parameters = set()
houseL = scrape_data(url)
dictionary = {}

for i in houseL:
    for j in i:
        parameters = parameters | set(i)


for i in parameters:
    data = []
    for j in houseL:
        data.append(j.get(i,'Not Known'))
    dictionary[i] = data

df = pd.DataFrame(dictionary)
df.to_csv('data.csv')
