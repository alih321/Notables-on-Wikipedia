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
    
    getPersonInformation(response)


def getPersonInformation(response):
    
    
    soup = BeautifulSoup(response, "lxml")
    
    #Simple Information (Name, YoB, YoD)
    name = soup.find_all("h1")[0].text
    
    infoData = soup.find_all(class_="infobox-data")

    bornDate = infoData[0].find("br").previous.strip()
    deathDate = infoData[1].find("span").previous.strip()
    
    print(name, bornDate, deathDate)     
    
    #Get all links in Tuple
    #allLinks = []
    
    #bodyContentChildren = soup.find("div", {"id" : "bodyContent"})
    #print(bodyContentChildren)
    
    #for link in bodyContentChildren[0]:
     #   if link.has_attr("href"):
      #      allLinks.append((link.string, link["href"]))
    

        
        
    
if __name__ == "__main__":
    main();