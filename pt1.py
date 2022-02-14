#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 20:53:08 2022
@authors: alihachem LucAlexander
"""

from bs4 import BeautifulSoup;
from urllib.request import urlopen;
import csv
import time

def main():
    depth = 3
    #seed = "https://en.wikipedia.org/wiki/Luc_Bourdon"
    seed = "https://en.wikipedia.org/wiki/Muhammad_Ali"
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
            crawl(source, url, nextDepth, personInfo, linkConnections)
        # if all urls at a depth have been crawled, append all data to master urls list
        # clear temprorary url storage
        if i == len(urls)-1:
            print("layer " + str(3-depth) + " completed")
            urls += nextDepth
            nextDepth = list()
            depth -= 1
    linkConnections = linkConnections[1:]
    print("Crawling finished")
    print(linkConnections)
    print(personInfo)
    print("Writing to CSV")
    with open("links.csv", "w+") as infilecsv:
        writer = csv.writer(infilecsv)
        writer.writerow(["from_url","to_url"])
        for row in linkConnections:
            parsed = list(row)
            for i, item in enumerate(parsed):
                parsed[i] = item[30:]
            writer.writerow(parsed)
    with open("notables.csv", "w+") as infilecsv:
        writer = csv.writer(infilecsv)
        writer.writerow(["url","name","born","died"])
        for key in personInfo:
            writer.writerow(tuple([key])+personInfo[key])
    print("Writing to CSV finished")

def crawl(source, url, nextDepth, personInfo, linkConnections):
    soup = getSoupFromUrl(url)
    parsedUrl = url[30:] # get name from wikipedia link
    # we make sure not to download the url again if already parsed
    if parsedUrl not in personInfo:
        info = getPersonInformation(soup)
        if info == False:
            return
        personInfo[parsedUrl] = info
    # regardless of visited or not, store as tuple in final list
    linkConnections.append(tuple([source, url]))
    # add to temprary url storage medium
    nextDepth += getAllLinksFromPage(url, soup)

def getSoupFromUrl(url):
    response = urlopen(url)
    soup = BeautifulSoup(response, "lxml")
    return soup

def getPersonInformation(soup):
    
    #Simple Information (Name, YoB, YoD)
    
    if not checkPageSignificance(soup):
        print("NOT SIGNIFICANT!", soup.url)
        return False;
    
    name = soup.find_all("h1")[0].text
    
    bornLabel = soup.find(class_="infobox-label", string="Born")
    deathLabel = soup.find(class_="infobox-label", string="Died")
    
    bornDate = bornLabel.next.next.text.strip()
    deathDate = deathLabel.next.next.text.strip()
    print(bornLabel.next.next.text, "\n\n")
    print(deathLabel.next.next.text, "\n\n")
    
    return (name, bornDate, deathDate)


def checkPageSignificance(soup):
    return ((soup.find(class_="infobox-label", string="Born") is not None) and (soup.find(class_="infobox-label", string="Died") is not None))
        

def getAllLinksFromPage(source, soup):
    #Get all links in Tuple
    allLinks = []
    bodyContent = soup.find("div", {"id": "bodyContent"})
    for tag in bodyContent.find_all("a"):
        if tag.has_attr("href"):
            pulledUrl = tag.get("href")
            if (pulledUrl[:6] == "/wiki/"):
                pair = [source, "https://en.wikipedia.org" + pulledUrl]
                allLinks.append(tuple(pair)) 
    for links in allLinks:
        print(source + "->" + str(links[1]))
    return allLinks;

if __name__ == "__main__":
    main();
