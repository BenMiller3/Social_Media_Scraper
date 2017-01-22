from bs4 import BeautifulSoup
import requests
import re

def getFBname(name):
    name = name.replace(" ","+")
    url = "https://www.google.ca/search?q="+name+"+facebook+page"
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")

    x = soup.find("div", {"id": "ires"})
    hyper = x('a')[0]
    text = str(hyper)

    m = re.search('facebook.com/(.+?)&amp', text)
    if m:
        found = m.group(1)
    else:
        found = "no username found"

    return found.replace("/","")

def getTWname(name):
    name = name.replace(" ","+")
    url = "https://www.google.ca/search?q="+name+"+twitter"
    try:
        r = requests.get(url)
    except:
        return 00
    soup = BeautifulSoup(r.content,"html.parser")

    firstLink = soup.find("div", {"id": "ires"})
    hyperLink = firstLink('a')[0]
    line = str(hyperLink)

    m = re.search('twitter.com/(.+?)%',line)
    if m:
        username = m.group(1)
    else:
        # Add second catch search to find username
        url2 = "https://www.google.ca/search?q="+name+"+twitter+-hashtag+-news"
        try:
            r = requests.get(url2)
        except:
            return 00
        
        soup2 = BeautifulSoup(r.content,"html.parser")

        firstLink = soup2.find("div", {"id": "ires"})
        hyperLink = firstLink('a')[0]
        line = str(hyperLink)

        m = re.search('twitter.com/(.+?)&',line)
        
        if m:
            username = m.group(1)
        else:
            username = "no username found"

    return username.replace("/","")

def getIGname(name):
    name = name.replace(" ","+")
    url = "https://www.google.ca/search?q="+name+"+instagram"
    try:
        r = requests.get(url)
    except:
        return 00
    soup = BeautifulSoup(r.content,"html.parser")

    firstLink = soup.find("div", {"id": "ires"})
    hyperLink = firstLink('a')[0]
    line = str(hyperLink)

    m = re.search('instagram.com/(.+?)/',line)
    if m:
        username = m.group(1)
    else:
        username = "no username found"

    return username.replace("/","")


def getSocialMediaNames(name):
    fb = getFBname(name)
    tw = getTWname(name)
    ig = getIGname(name)
    line = str(name) + " " + str(fb) + " " + str(tw) + " " + str(ig)
    return line

def getFBLikes(username):
    url = "https://api.facebook.com/method/fql.query?query=select%20like_count%20from%20link_stat%20where%20url=%27http://facebook.com/" + username + "/%27&format=json"
    try:
        r = requests.get(url)
    except:
        print("Failed. Reason = unknown")

    soup = BeautifulSoup(r.content,"html.parser")
    text = str(soup)
    m = re.search(':(.+?)}', text)
    if m:
        found = m.group(1)
    else:
        found = 0
    return found

def getTWFollowers(username):
    url = "http://twitter.com/"+username
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        f = soup.find('li', class_="ProfileNav-item--followers")
        title = f.find('a')['title']
        num_followers = int(title.split(' ')[0].replace(',',''))
        return(num_followers)
    except:
        return(0)

def getIGFollowers(username):
    url = "http://benjaminmiller.co/spain/ig.php?name="+username
    try:
        r = requests.get(url)
    except:
        print("error")
    soup = BeautifulSoup(r.content,"html.parser")
    text = str(soup)
    m = re.search('\n(.+?)</body', text)
    if m:
        found = m.group(1)
    else:
        found = 0
    return found

def calculateSS(FB,TW,IG):
    x = float(FB)
    y = float(TW)
    z = float(IG)

    total = x + y + z

    ss = (total/1950000000)*1000

    return ss

def getSocialMediaNumbers(name):
    fb = getFBname(name)
    tw = getTWname(name)
    ig = getIGname(name)

    FB = getFBLikes(fb)
    TW = getTWFollowers(tw)
    IG = getIGFollowers(ig)

    SS = calculateSS(FB,TW,IG)

    line = str(name) + "," + str(FB) + "," + str(TW) + "," + str(IG) + "," + str(SS)
    return line

name = "Bernie Sanders"
name2 = "Donald Trump"
name3 = "Hillary Clinton"
name4 = "Jeb Bush"
name5 = "Ted Cruz"

print(getSocialMediaNumbers(name))
print(getSocialMediaNumbers(name2))
print(getSocialMediaNumbers(name3))
print(getSocialMediaNumbers(name4))
print(getSocialMediaNumbers(name5))
