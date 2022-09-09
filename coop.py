# %%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from tilbud import writer
from bs4 import BeautifulSoup
import pandas as pd
import time

# %%
def Coop(soup):
    names = soup.find_all(class_="text-10 md:text-12 text-grey-darker leading-tight product-text-truncate font-medium")
    words = soup.find_all(class_="c-product-tile__title hover:underline")
    Søgeord = soup.find_all(class_="u-text-blur")[1].text.split("Din søgning på ",1)[1].split(" ")[0].replace("'","")
    prices = soup.find_all(class_='price-wrap text-23 md:text-24 inline mb-5 font-medium')
    pricespr = soup.find_all(class_="text-grey-darker text-11 mb-5 font-medium")
    
    words = [word.text for word in words]
    PricesPr = [float(price.text.split()[0].replace(",",".").replace("-","")) for price in pricespr]
    Unit = [price.text.split(maxsplit=1)[1].replace("kr. ","").lower().replace(".", "") for price in pricespr]
    Brand = [name.text.replace("\n","").replace(" ","").split(",")[0] for name in names]
    Prices = [float(price.text[:-2] + "." + price.text[-2:]) for price in prices]
    Weight = [str(round(Prices[i]/PricesPr[i], 3)) +" "+ Unit[i].split()[-1] for i in range(len(Prices))]


    df = pd.DataFrame(columns=["Søgeord", "Pris", "Enhed", "Total Pris", "Butik", "Mængde", "Dato"])

    df["Søgeord"] = words
    df["Pris"] = PricesPr
    df["Enhed"] = Unit
    df["Total Pris"] = Prices
    df["Butik"] = Brand
    df["Mængde"] = Weight
    df["Dato"] = pd.to_datetime("today").strftime('%d.%m.%Y')
    df = df.drop_duplicates()
    return df, Søgeord

def main():
    CoopLinks = "coop_links.txt"
    vare = open(CoopLinks, "r")
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    for var in vare:
        driver.get(var)
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        df, Søgeord = Coop(soup)
        string = f"coop/{Søgeord}.txt"
        writer(string, df)

if __name__ == '__main__':
    print("Fetching")
    main()
    print("Fetching complete") 
    exit()
        
# %%

#CoopLinks = "links.txt"
#vare = open(CoopLinks, "r")
driver = webdriver.Firefox()
var = "https://mad.coop.dk/frost/frugt-og-groent/c-571?term=jordb%C3%A6r&tab=products&categories=571&lastFacet=categories"
#var = "https://mad.coop.dk/frost/frugt-og-groent/c-571?term=bl%C3%A5b%C3%A6r&tab=products&categories=562&lastFacet=categories"

driver.get(var)
soup = BeautifulSoup(driver.page_source, "html.parser")

# %%
names = soup.find_all(class_="text-10 md:text-12 text-grey-darker leading-tight product-text-truncate font-medium")
Søgeord = soup.find_all(class_="u-text-blur")[1].text.split("Din søgning på ",1)[1].split(" ")[0].replace("'","")
prices = soup.find_all(class_='price-wrap text-23 md:text-24 inline mb-5 font-medium')
pricespr = soup.find_all(class_="text-grey-darker text-11 mb-5 font-medium")

PricesPr = [float(price.text.split()[0].replace(",",".")) for price in pricespr]
Unit = [price.text.split(maxsplit=1)[1] for price in pricespr]
Brand = [name.text.replace("\n","").replace(" ","").split(",")[0] for name in names]
Prices = [float(price.text[:-2] +"." + price.text[-2:]) for price in prices]
Weight = [str(round(Prices[i]/PricesPr[i], 3)) +" "+ Unit[i].split()[-1] for i in range(len(Prices))]

# %%
####################### REMA1000
søgeord = "jordbær"
var = "https://shop.rema1000.dk/frost/grontsagerfrugt-og-baer"
driver.get(var)

# %%
soup = BeautifulSoup(driver.page_source, "html.parser")
# %%

names = soup.find_all(class_="title")[1:-2]
prices = soup.find_all(class_="price")
brand = soup.find_all(class_="extra")

ind = [i for i in range(len(names)) if names[i].text.lower()==søgeord.lower()]
Prices = [float(prices[i].text.split()[0][:-2] + "." + prices[i].text.split()[0][-2:]) for i in ind]
PricesPr = [float(prices[i].text.split()[1]) for i in ind]
Unit = [prices[i].text.split(maxsplit=2)[-1] for i in ind]
Weight = [str(round(Prices[i]/PricesPr[i], 3)) +" "+ Unit[i].split()[-1] for i in range(len(Prices))]
Brand = [brand[i].text.split("/")[-1][1:] for i in ind]

# %%
df = pd.DataFrame(columns=["Søgeord", "Pris", "Enhed", "Total Pris", "Butik", "Mængde", "Dato"])

df["Søgeord"] = søgeord
df["Pris"] = PricesPr
df["Enhed"] = Unit
df["Total Pris"] = Prices
df["Butik"] = Brand
df["Mængde"] = Weight
df = df.drop_duplicates()
df["Dato"] = pd.to_datetime("today").strftime('%d.%m.%Y')

