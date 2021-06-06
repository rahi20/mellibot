# Scrape address cards from http://smedian.ma/endocrinos/
#create a csv file with all the records

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

browser = webdriver.Chrome('./chromedriver')
browser.get('http://smedian.ma/endocrinos/')

results = browser.find_elements_by_class_name('address-card')

dic = {
    'id' : [],
    'name' : [],
    'sector' : [],
    'email' : [],
    'tel' : [],
    'address' : [],
    'city' : []
}

k = 1
for res in results:
    dic['id'].append(k)
    k+=1

    lines = res.text.splitlines()
    dic['name'].append(lines[0])

    dic['sector'].append("" if len(lines[1].split(" : "))==1 else 'private' if lines[1].split(" : ")[1] == 'Privé' else 'public')
    dic['email'].append("" if len(lines[2].split(" : "))==1 else lines[2].split(" : ")[1])
    dic['tel'].append("" if len(lines[3].split(" : "))==1 else lines[3].split(" : ")[1])

    #address can be on multiple lines -> splitlines doesn't return the desired output.

    i = res.text.find('Adresse')
    j = res.text.find('Ville')
    adr = res.text[i:j].strip()
    dic['address'].append("" if len(adr.split(" : "))==1 else adr.split(" : ")[1])

    dic['city'].append("" if len(lines[-1].split(" : "))==1 else lines[-1].split(" : ")[1])


data = pd.DataFrame.from_dict(dic)
data.to_csv("endocrinos.csv", index=False)
