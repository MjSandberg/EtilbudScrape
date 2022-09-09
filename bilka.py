# %%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from tilbud import writer
from bs4 import BeautifulSoup
import pandas as pd
import time
# %%

def bilka(soup):
    names = soup.find_all(class_="row product-description flex-column")
    prices = soup.find_all(class_="product-price h1 d-flex md")
    brand = soup.find_all(class_="description")

    Søgeord = soup.find(class_="m-0 text-center").text.replace('“','').replace('”','').split()[0]
    ind = [i for i in range(len(names)) if Søgeord.lower() in names[i].text.lower()]
    Prices = [float((prices[i].text.split()[0] + "." + prices[i].text.split()[1]).replace(".-","")) for i in ind]
    PricesPr = [float(brand[i].text.split()[-1].split("/")[0].replace(",","."))  for i in ind]
    Unit = ["pr " + brand[i].text.split()[-1].split("/")[1].lower().replace(".","") for i in ind]
    Weight = [str(round(Prices[i]/PricesPr[i], 3)) +" "+ Unit[i].split()[-1] for i in range(len(Prices))]
    Names = [names[i].text.split()[0] for i in ind]
    Brand = [brand[i].text.split()[0] for i in ind]

    df = pd.DataFrame(columns=["Søgeord", "Pris", "Enhed", "Total Pris", "Butik", "Mængde", "Dato"])
    df["Søgeord"] = Names
    df["Pris"] = PricesPr
    df["Enhed"] = Unit
    df["Total Pris"] = Prices
    df["Butik"] = Brand
    df["Mængde"] = Weight
    df["Dato"] = pd.to_datetime("today").strftime('%d.%m.%Y')
    df = df.drop_duplicates()

    return df, Søgeord
# %%
def main():
    vare = open("bilka_links.txt", "r")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    for var in vare:
        driver.get(var)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
            
        df, Søgeord = bilka(soup)
        string = f"bilka/{Søgeord}.txt"
        writer(string, df)
        
if __name__ == '__main__':
    print("Fetching")
    main()
    print("Fetching complete") 
    exit()