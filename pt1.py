"""
Created on Fri Feb 11 20:53:08 2022
@authors: alihachem LucAlexander
"""

from bs4 import BeautifulSoup;
from urllib.request import urlopen;
import csv
import re

def getSoupFromUrl(url):
    response = urlopen(url)
    soup = BeautifulSoup(response, "lxml")
    return soup

def getPersonInformation(soup):
    
    #Simple Information (Name, YoB, YoD)
    
    if not checkPageSignificance(soup):
        #not significant
        return False;
    
    name = soup.find_all("h1")[0].text
    
    bornLabel = soup.find(class_="infobox-label", string="Born")
    deathLabel = soup.find(class_="infobox-label", string="Died")
    
    bornDate = bornLabel.next.next.text.strip()
    deathDate = deathLabel.next.next.text.strip()
    
    bornMatch = re.search("\d\d\d+", bornDate)
    deathMatch = re.search("\d\d\d+", deathDate)
    
    yod = None
    yob = None
    
    if (bornMatch is not None):
        yob = bornMatch.group()
    else:
        return False
    
    if (deathMatch is not None):
        yod = deathMatch.group()
    else:
        return False
        
    return (name, yob, yod)

def checkPageSignificance(soup):
    return ((soup.find(class_="infobox-label", string="Born") is not None) and (soup.find(class_="infobox-label", string="Died") is not None))

def getAllLinksFromPage(soup):
    # get all links in page
    allLinks = []
    bodyContent = soup.find("div", {"id": "bodyContent"})
    for tag in bodyContent.find_all("a"):
        if tag.has_attr("href"):
            pulledUrl = tag.get("href")
            if (pulledUrl[:6] == "/wiki/"):
                pair = "https://en.wikipedia.org" + pulledUrl
                allLinks.append(pair) 
    return allLinks;
       
def crawl(source, url, depth, startDepth, infoData, linkData):
    if depth < 0:
        return
    soup = getSoupFromUrl(url)
    parsedUrl = url[30:] # get name from wikipedia link
    if parsedUrl not in infoData:
        info = getPersonInformation(soup)
        if info == False:
            return
        infoData[parsedUrl] = info
        links = getAllLinksFromPage(soup)
        for i, suburl in enumerate(links):
            crawl(url, suburl, depth-1, startDepth, infoData, linkData)
            if depth == startDepth:
                print("\r\tPROGRESS [\033[1;31m", end="")
                k = 0
                while(k < ((i/len(links))*100)):
                    print("#",end="")
                    k+=1
                while(k<100):
                    print(" ",end="")
                    k+=1
                print("\033[0m]",(i*100)//len(links),"%",end="")
    linkData.append(tuple([source, url]))

def writeToCsv(infoData, linkData):
    with open("links.csv", "w+") as infilecsv:
        writer = csv.writer(infilecsv)
        writer.writerow(["from_url","to_url"])
        for row in linkData:
            parsed = list(row)
            for i, item in enumerate(parsed):
                parsed[i] = item[30:]
            writer.writerow(parsed)
    with open("notables.csv", "w+") as infilecsv:
        writer = csv.writer(infilecsv)
        writer.writerow(["url","name","born","died"])
        for key in infoData:
            writer.writerow(tuple([key])+infoData[key])

def main():
    infoData = dict()
    linkData = list()
    seed = "https://en.wikipedia.org/wiki/Luc_Hoffmann"
    startDepth = 2
    depth = startDepth
    print("\n\tCrawling ", seed, " at depth ", startDepth, "\n")
    crawl(seed, seed, depth, startDepth, infoData, linkData)
    writeToCsv(infoData, linkData)
    print("\n\tDone")

if __name__=="__main__":
    main()


