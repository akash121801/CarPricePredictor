from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from sklearn import linear_model
from dateutil.parser import parse
import re
import locale


URL="https://cnj.craigslist.org/d/cars-trucks-by-owner/search/cto" 
driver=webdriver.Chrome(executable_path="C:\\Users\\akash\\Downloads\\chromedriver.exe")
driver.get(URL)

time.sleep(8)

html=driver.page_source
soup= BeautifulSoup(html, 'html.parser')
content=soup.find(class_="rows")

df=pd.DataFrame()
car_elements=content.find_all('li', class_="result-row")

for car_elem in car_elements:
 
    link=car_elem.find('a', class_="result-image gallery")
    
    if link is not None:
        price_elem=car_elem.find('span', class_='result-price')
        car_model=car_elem.find('a', class_='result-title hdrlnk')
        driver.get(link.get('href'))
        car_html=driver.page_source 
        car_soup=BeautifulSoup(car_html, 'html.parser')
        attributes=car_soup.find_all('p', class_='attrgroup')
        if (len(attributes) > 1):
            attrs=attributes[1]
            spans=attrs.find_all('span')

            info_list=[]
            for span in spans:
                if(span.text.strip().find(":") != -1):
                    info_list.append(span.text.strip())
            
            d=dict(x.split(":") for x in info_list) #Contains important data about the car itself

            d['Car Model']=car_model.text.strip()
            d['Price']=price_elem.text.strip()
            df=df.append(d, ignore_index=True)
            print(d)

#Cleaning the data up
for col in df.columns:
    print(col)

df= df.drop(columns=['VIN', 'paint color'])
df=df.reset_index()


#Extracting year from the Car Model
for car in df['Car Model']:
    try:
        year = parse(car, fuzzy=True).year
        df=df.replace([car], year)
    except:
        df=df.drop(df[df['Car Model']== car].index.values)


locale.setlocale(locale.LC_ALL,'')
df['Price']=df.Price.map(lambda x: locale.atof(x.strip('$')))

print(df.head())

#Analysis

X=df[['Car Model','odometer']]
y=df['Price']

regr=linear_model.LinearRegression()
regr.fit(X,y)

car_year=int(input('Enter the year of the car you want to buy.'))
miles=int(input('How many miles are on the car you want to buy?'))

predicted_Price=regr.predict([[car_year, miles]])
print("Predicted price of your car is: " + predicted_Price)





        
            
            
    

 
