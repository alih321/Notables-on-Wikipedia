#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 20:53:08 2022

@author: alihachem
"""

from bs4 import BeautifulSoup;
from urllib.request import urlopen;

def main():
    url = "https://en.wikipedia.org/wiki/Luc_Bourdon"
    response = urlopen(url)
    soup = BeautifulSoup(response, "lxml")

    if getPersonInformation(soup) != False:
        getAllLinksFromPage(soup)


def getPersonInformation(soup):
    
    #Simple Information (Name, YoB, YoD)
    name = soup.find_all("h1")[0].text
    
    infoLabels = soup.find_all(class_="infobox-label")
    infoData = soup.find_all(class_="infobox-data")
    
    
    #Test for YoD labeled    
    if "Died" in map(lambda l : l.get_text(), infoLabels):
        print("Found!")
    else:
         print("No death date!") 
         return False #Handle as you will. Just placeholder. I know this is one of Zinoviev's sins


    # Hard coded. My initial thought is to find the first instance of "Born" / "Died" in infoLabel
    # and use that index on infoData. Just don't have time right now.
    bornDate = infoData[0].find("br").previous.strip() 
    deathDate = infoData[1].find("span").previous.strip()
    
    print(name, bornDate, deathDate)
    
    return (name, bornDate, deathDate)

        

def getAllLinksFromPage(soup):
        
    #Get all links in Tuple
    allLinks = []
            
    bodyContent = soup.find("div", {"id": "bodyContent"})
    
    for tag in bodyContent.find_all("a"):
        if tag.has_attr("href"):
            allLinks.append((tag.string, tag["href"]))
            
    for link in allLinks:
        print(link)
        print("\n")
    
    return allLinks;
    

        
        
    
if __name__ == "__main__":
    main();