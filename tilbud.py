# %%
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
from requests import get, Session
from bs4 import BeautifulSoup
import re
from os.path import exists

geocook = '{"position":{"coordinates":{"latitude":55.68149332511764,"longitude":12.563273460788182,"accuracy":100},"timestamp":1658859974896,"source":"google.maps"},"address":{"formattedAddress":"Turesensgade 17, 1368 København, Danmark","countryCode":"DK","timestamp":1658859974896,"source":"google.maps"},"searchRadius":600,"searchRadiusSource":"user"}'

sgn_preferences = '{"orderBy":"unit_price_asc","offers":{"includeUpcoming":false}}'
sgn_i18n = '{%22locale%22:%22da-DK%22}'

def EtilbudSearchScrape(search, geocook, sgn_preferences, sgn_i18n):
    url = f"https://etilbudsavis.dk/soeg/{search}" + "?ordered_by=unit_price_asc&include_upcoming=false"
    s = Session()
    txt = s.get(url, cookies={"sgn-geo": geocook, "sgn-preferences":sgn_preferences, "sgn-i18n": sgn_i18n}).text
    soup = BeautifulSoup(txt,"html.parser")

    df = pd.DataFrame(columns=["Søgeord", "Pris", "Enhed", "Total Pris", "Navn", "Butik", "Mængde", "Dato"])

    links = soup.find_all(attrs={'class': "UniversalCardList__Card-sc-4v1xeg-2"})
    links = np.array(["https://etilbudsavis.dk" + link["href"] for link in links])

    prisEnhedArr = []
    enhedArr = []
    mængdeArr = []
    prisArr = []
    navnArr = []
    butikArr = []
    datoArr = []

    for link in links:
        url = f"{link}"
        s = Session()
        txt = s.get(url, cookies={"sgn-geo": geocook, "sgn-preferences":sgn_preferences, "sgn-i18n": sgn_i18n}).text
        soup = BeautifulSoup(txt,"html.parser")

        tags = soup.find(attrs={"class": "OfferPriceTag__BlockPrice-sc-1cl0fuo-2 cvzFOb"})
        for i in tags:
            if "før" in i.string.lower() or "spar" in i.string.lower():
                continue
            else: 
                pris = float(i.string.split()[0].replace(",","."))
                
        prisEnhed = soup.find_all(attrs={"class": "OfferDetailsDescription___StyledUl-sc-10nqfi3-1 dJoozi"})[0].text.replace("max ", "")
        if prisEnhed:
            res = re.findall(r"[^\W\d_]+|\d+", prisEnhed.split()[1])
            if len(res)==1:
                enhed = res[0]
                mængde = float(prisEnhed.replace(enhed, ""))
            else:
                enhed = res[0] + "/" + res[1]
                mængde = float(res[2])
            
            findPris = re.findall(r"\d+,\d+", prisEnhed)
            if len(findPris) > 0:
                prisEnhed = float(findPris[0].replace(",","."))
            else:
                prisEnhed = pris
                

        else: 
            # Hardcoded at hvis der ikke er nogen underlinje med info at det nok er 1 stk.
            prisEnhed = pris
            mængde = 1.0
            enhed = "stk."            

        navnMm = soup.find_all(attrs={"class": "Card-sc-x265nh-0 OfferDetailsDescription__OfferInfo-sc-10nqfi3-0 bVNBDA UPrPp OfferDetails___StyledOfferDetailsDescription-sc-v2wdtj-7 gQCOTg"})[0].text
        butik = soup.find_all(attrs={"class": "BusinessLabel__BusinessLabelDiv-sc-iksnba-0 hjwtkA"})[0].text
        ind = np.where(np.array([a.isnumeric() for a in navnMm]) == True)[0]
        navn = navnMm[:ind[0]]

        if len(navn)==0:
            # Hardcoded at hvis der er tal i starten af navnet så er det nok fra 365 og dermed 3 tal i starten.
            navn = navnMm[:ind[3]]
        
        upper = soup.find(attrs={"class": "Card-sc-x265nh-0 OfferDetailsPrice___StyledCard-sc-pbamha-0 bVNBDA jRMmut OfferDetails___StyledOfferDetailsPrice-sc-v2wdtj-6 hCIKEJ"})
        text = upper.find("span").get("title")
        dato = pd.to_datetime(text.split()[-1],dayfirst=True, format="%d.%m.%Y")

        prisEnhedArr.append(prisEnhed)
        enhedArr.append(enhed)
        mængdeArr.append(mængde)
        prisArr.append(pris)
        navnArr.append(navn)
        butikArr.append(butik)
        datoArr.append(dato)
        

    df["Pris"] = prisEnhedArr
    df["Enhed"] = enhedArr
    df["Mængde"] = mængdeArr
    df["Total Pris"] = prisArr
    df["Navn"] = navnArr
    df["Butik"] = butikArr
    df["Dato"] = pd.to_datetime(datoArr, dayfirst=True, format="%d.%m.%Y")
    df["Søgeord"] = search

    df["Dato"] = df["Dato"].dt.strftime('%d.%m.%Y')

    if len(prisEnhedArr)==0:
        print("Ingen aktuelle tilbud")

    return df


# %%

def writer(file, df):
    import os 
    if exists(file):
        
        df.to_csv("temp", index=False)
        dfOld = pd.read_csv(file)
        df = pd.read_csv("temp")
        dfNew = df.append(dfOld)
        dfNew = dfNew.drop_duplicates()
        dfNew.to_csv(file, index=False)
        
        os.remove("temp")
        
    else:
        df.to_csv(file, index=False)

def main():
    geocook = '{"position":{"coordinates":{"latitude":55.68149332511764,"longitude":12.563273460788182,"accuracy":100},"timestamp":1658859974896,"source":"google.maps"},"address":{"formattedAddress":"Turesensgade 17, 1368 København, Danmark","countryCode":"DK","timestamp":1658859974896,"source":"google.maps"},"searchRadius":600,"searchRadiusSource":"user"}'
    sgn_preferences = '{"orderBy":"unit_price_asc","offers":{"includeUpcoming":false}}'
    sgn_i18n = '{%22locale%22:%22da-DK%22}'

    searches = "tilbud.txt"
    tilbud = open(searches, "r").read().replace("Ã¥", "å").replace("Ã¦","æ").replace("Ã¸","ø").split("\n")

    #Etilbudsavis
    for search in tilbud:
        file = f"tilbud_data/{search}.txt"
        print("searching: ", search)
        df = EtilbudSearchScrape(search, geocook, sgn_preferences, sgn_i18n)
        writer(file, df)
        
if __name__ == '__main__':
    print("Fetching")
    main()
    print("Fetching complete")
    exit()
