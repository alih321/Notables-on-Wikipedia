#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 20:53:08 2022

@authors: alihachem LucAlexander
"""

from bs4 import BeautifulSoup;
from urllib.request import urlopen;

def main():
    depth = 2
    seed = "https://en.wikipedia.org/wiki/Luc_Bourdon"
    seedTup = tuple([seed, seed])
    urls = [seedTup] # master list of urls
    linkConnections = list() # final list of extracted links in tuple form (source, destination)
    personInfo = dict() # final dictionary of person information to be exported to csv
    nextDepth = list() # temporary url storage 
    # Read through collected links as tuples containing (source, destination)
    # this starts as (seed, seed)
    for i, urlPair in enumerate(urls):
        source = urlPair[0]
        url = urlPair[1]
        if depth > 0:
            crawl(source, url, nextDepth, personInfo)
        # if all urls at a depth have been crawled, append all data to master urls list
        # clear temprorary url storage
        if i == len(urls)-1:
            urls += nextDepth
            nextDepth = list()
            depth -= 1
    # TODO export to CSV


def crawl(source, url, nextDepth, personInfo, linkConnections):
    soup = getSoupFromUrl(url)
    parsedUrl = url[30:] # get name from wikipedia link
    # we make sure not to download the url again if already parsed
    if parsedUrl not in personInfo 
        info = getPersonInformation(soup)
        if info == False:
            return
        personInfo[parsedUrl] = info
    # regardless of visited or not, store as tuple in final list
    linkConnections.append(tuple([source, url]))
    # add to temprary url storage medium
    nextDepth += getAllLinksFromPage(source, soup)

def getSoupFromUrl(url):
    response = urloen(url)
    soup = BeautifulSoup(response, "lxml")
    return soup

def getPersonInformation(soup):
    
    #Simple Information (Name, YoB, YoD)
    name = soup.find_all("h1")[0].text
    
    infoLabels = soup.find_all(class_="infobox-label")
    infoData = soup.find_all(class_="infobox-data")
    
    
    #Test for YoD labeled    
    if "Died" in map(lambda l : l.get_text(), infoLabels):
        print("Found!")
    else:
        print("No year of death found")
        return False


    # Hard coded. My initial thought is to find the first instance of "Born" / "Died" in infoLabel
    # and use that index on infoData. Just don't have time right now.
    bornDate = infoData[0].find("br").previous.strip() 
    deathDate = infoData[1].find("span").previous.strip()
    
    print(name, bornDate, deathDate)
    
    return (name, bornDate, deathDate)

def getAllLinksFromPage(souce, soup):

    #Get all links in Tuple
    allLinks = []
            
    bodyContent = soup.find("div", {"id": "bodyContent"})
   
    for tag in bodyContent.find_all("a"):
        if tag.has_attr("href"):
            pair = [source, (tag.string, tag["href"])]
            allLinks.append(tuple(pair)) 
    for links in allLinks:
        print(links[0] + "->" + links[1])
        print("\n")
    
    return allLinks;

if __name__ == "__main__":
    main();
