# %%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from tilbud import writer
from bs4 import BeautifulSoup
import pandas as pd
import time

# %%

def REMA(soup, søgeord):
    ####################### REMA1000
    names = soup.find_all(class_="title")[1:-2]
    prices = soup.find_all(class_="price")
    brand = soup.find_all(class_="extra")

    ind = [i for i in range(len(names)) if søgeord.lower() in names[i].text.lower()]
    Søgeord = [names[i].text for i in ind]
    Prices = [float(prices[i].text.split()[0][:-2] + "." + prices[i].text.split()[0][-2:]) for i in ind]
    PricesPr = [float(prices[i].text.split()[1]) for i in ind]
    Unit = [prices[i].text.split(maxsplit=2)[-1].replace("per","pr").lower().replace(".", "") for i in ind]
    Weight = [str(round(Prices[i]/PricesPr[i], 3)) +" "+ Unit[i].split()[-1] for i in range(len(Prices))]
    Brand = [brand[i].text.split("/")[-1][1:] for i in ind]

    df = pd.DataFrame(columns=["Søgeord", "Pris", "Enhed", "Total Pris", "Butik", "Mængde", "Dato"])

    df["Søgeord"] = Søgeord
    df["Pris"] = PricesPr
    df["Enhed"] = Unit
    df["Total Pris"] = Prices
    df["Butik"] = Brand
    df["Mængde"] = Weight
    df["Dato"] = pd.to_datetime("today").strftime('%d.%m.%Y')
    df = df.drop_duplicates()
    return df
# %%
def main():
    Søgeord = open("rema_søgeord.txt", "r").read().replace("Ã¥", "å").replace("Ã¦","æ").replace("Ã¸","ø").split("\n")
    vare = open("rema_links.txt", "r")
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    for var, søgeord in zip(vare, Søgeord):
        #wait = WebDriverWait(driver, timeout=10)
        driver.get(var)
        #wait.until(EC.url_to_be(var))
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #driver.quit()
        
        df = REMA(soup, søgeord)
        string = f"rema/{søgeord}.txt"
        writer(string, df)
        
if __name__ == '__main__':
    print("Fetching")
    main()
    print("Fetching complete") 
    exit()
    
# %%
søgeord = "mælk"
#var = "https://shop.rema1000.dk/mejeri/maelk-mv?filters=lactose_free"
var = "https://www.bilkatogo.dk/s?query=m%C3%A6lk%20laktosefri"
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(var)

# %%
soup = BeautifulSoup(driver.page_source, "html.parser")
# %%

names = soup.find_all(class_="title")[1:-2]
prices = soup.find_all(class_="price")
brand = soup.find_all(class_="extra")

ind = [i for i in range(len(names)) if søgeord.lower() in names[i].text.lower()]
Prices = [float(prices[i].text.split()[0][:-2] + "." + prices[i].text.split()[0][-2:]) for i in ind]
PricesPr = [float(prices[i].text.split()[1]) for i in ind]
Unit = [prices[i].text.split(maxsplit=2)[-1] for i in ind]
Weight = [str(round(Prices[i]/PricesPr[i], 3)) +" "+ Unit[i].split()[-1] for i in range(len(Prices))]
Brand = [brand[i].text.split("/")[-1][1:] for i in ind]
# %%
