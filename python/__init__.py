import urllib
import pprint
import re
import csv

def getData(url=None):
    if url is None:
        url = "https://filmfreeway.com/TheGreatOffensiveInternationalShortFilmFestival"
    data = {}

    page = urllib.urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    # Title
    pattern = "<meta property=\"og:title\" content=\"(.*?)\">"
    match_results = re.search(pattern, html, re.IGNORECASE)
    if match_results:
        grup = match_results.groups()[0]
        data["Title"] = grup
    else:
        data["Title"] = None

    #Country
    pattern = "href=\"https:\/\/maps.google.com\/(.*?)>"
    match_results = re.search(pattern, html, re.IGNORECASE)
    if not match_results:
        data["Country"] = None
        data["Region"] = None
    else:
        grps = match_results.groups()
        if grps:
            location = grps[0].rsplit("+")
            country =  location[-1].replace("\"", "").strip()
            rawRegion = " ".join(location[:-1]).replace("?q=", "")
            region = urllib.unquote(rawRegion)
            if country == "States":
                country = "USA"
            data["Country"] = country
            data["Region"] = region
 
    #Dates
    pattern = "Dates &amp; Deadlines([\S\s\d]*?)<div class=\"Section-component\">"
    match_results = re.search(pattern, html, re.IGNORECASE)
    dates = {}
    if match_results:
        grps = match_results.groups()
        date = None
        if grps:
            found = grps[0]
            lines = found.split("\n")
            lenLines = len(lines)
            i = 0
            while i < lenLines:
                if "datesDeadlines-time" in lines[i]:
                    date=lines[i+1].replace("&ndash;", "-")
                elif "datesDeadlines-deadline" in lines[i]:
                    name = re.sub(' +', ' ', lines[i+1]).strip()
                    if "Deadline" in name or "Event" in name:
                        dates[name] = re.sub(' +', ' ', date).strip()
                i+=1
    data["Dates"] = dates


    #Award
    pattern = "Awards &amp; Prizes([\S\s\d]*?)<\/section>"
    match_results = re.search(pattern, html, re.IGNORECASE)
    clean = re.compile("<.*?>")
    if match_results:
        found = match_results.groups()[0]
        lines = found.split("\n")
        text = []
        start=False
        for x in lines:
            if"</p>" in x and start:
                break
            if "<p>" in x:
                start = True
            if start:
                notags = re.sub(clean, "", x )
                nospaces = re.sub(" +", " ", notags)
                stripped = re.sub("\s+", " ", nospaces).strip()
                text.append(stripped)

        data["Awards"] = " ".join(text)
    else:
        data["Awards"] = None

    #Regs

    #Process

    # #Additional info
    # pattern = "<li><span class=\"icon icon-globe\">(.*?)<\/a>"
    # match_results = re.search(pattern, html, re.IGNORECASE)
    # if match_results:
    #     grps = match_results.groups()
    #     print(grps)
    # else:
    #     print("NO")

    #Organizers

    pattern = "<div aria-level=\"5\" class=\"ProfileFestival-sidebarHeader\" role=\"heading\">([\S\s\d]*?)<\/ul>"
    match_results = re.search(pattern, html, re.IGNORECASE)  
    if match_results:
        found = match_results.groups()[0]
        nospaces = re.sub(" +", " ", found)
        stripped = re.sub("\s+", " ", nospaces).strip()
        notags = re.sub(clean, "", stripped)
        eventType = re.sub(" +", " ", notags).replace("Event Type ", "")
        data["EventType"] = eventType
    else:
        data["EventType"] = None
    #Category
    #USD
    #USD at final
    return data


def getFests(url=None):
    # Get urls for fests from webpage

    
    urls = ["https://filmfreeway.com/cinema35",
            "https://filmfreeway.com/AdventureMovieAwards",]
    types = []
    country = []
    region = []
    dates = []
    info = []

    for url in urls :
        data = getData(url = url)
        types.append(data["EventType"])
        country.append(data["Country"])
        region.append(data["Region"])
        for k, v in data["Dates"].iteritems():
            dates.append("%s : %s" % (k,v))
        info.append(data["Awards"])
        #Do csv

    for x in [types, country, region, dates, info]:
        for y in x:
            print(y)
        print("")


getFests()




