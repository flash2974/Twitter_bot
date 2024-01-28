from ntscraper import Nitter
import datetime
scraper = Nitter()
    
def last10TweetLink(profile, n = 10) :
    "returns {url : [], date : []} of last 10 tweets"
    try : 
        tweets = scraper.get_tweets(profile, mode='user', number = n)
    except Exception as e : print(e)

    else : 
        if len(tweets['tweets']) != 10 : raise Not10Tweets('10 tweets supposed to be returned, but not the case (causing error)')
        if pinnedTweet(tweets) :
            start = 1  
        else : 
            start = 0
        
        urls = []
        for indice in range(start, len(tweets['tweets'])) :
            if not tweets['tweets'][indice]['is-retweet'] : 
                urls.append(tweets['tweets'][indice]['link'])

        return urls
 
def newTweet(profile) :
    try :
        newList = last10TweetLink(profile)
    except Not10Tweets : raise Not10Tweets('10 tweets supposed to be returned, but not the case (causing error)')

    with open("TweetsData.txt", "r", encoding="utf-8") as file :
        oldList = eval(file.read().strip())
        file.close()
        
    if newList == [] : return [False]
    if oldList == [] and len(newList) > 0 : return [True, newList]
        
    #If no new tweet has been posted
    if oldList[0] == newList[0] : return [False]
    
    i = 1
    while newList[i] != oldList[0] and i < len(newList) :
        i += 1
        
    newTweets = newList[0:i]
    res = [True, newTweets]
    oldList = newList + oldList
    oldList = clearList(oldList)
    with open("TweetsData.txt", "w", encoding="utf-8") as file :
        file.write(str(oldList))
        file.close()
    return res #res = [True, [url1, url2]] ou [False]

def init(profile) :
    try :
        lastTweet = last10TweetLink(profile)
    except IndexError :
        init(profile)
    else :
        with open("TweetsData.txt", "w", encoding="utf-8") as file :
            file.write(str(lastTweet))
            file.close()
    
def addFx(link) :
    link = link.split('https://')[1]
    res = 'https://fx' + link
    return res

def pinnedTweet(tweets) :
    if len(tweets['tweets']) != 10 : 
        raise IndexError('10 tweets supposed to be returned, but not the case (causing IndexError)')
    dateTweet1 = transformDate(tweets['tweets'][0]['date'])
    dateTweet2 = transformDate(tweets['tweets'][1]['date'])
    print('tweet epingle' if dateTweet1 < dateTweet2 else 'tweet non epingle')
    return dateTweet1 < dateTweet2 #if the first tweet is older than the second, then the first is pinned


def transformDate(date : str) :
    '''Transforms a date in this format : 'MMM JJ, AAAA · HH:MM A/PM UTC to a datetime object'''
    hourMinutes = date.split(' · ')[1].split(':')
    if 'PM' in hourMinutes[1] : 
        minutes = int(hourMinutes[1].split(' PM')[0])
        hour = int(hourMinutes[0]) + 12
    
    else : 
        minutes = int(hourMinutes[1].split(' AM')[0])
        hour = int(hourMinutes[0])

    day = date[4:6]
    month = date[0:3]
    year = date[8:12]
    if not day.isdigit() : 
        day = date[4:5]
        year = date[7:11] 
    day = int(day)
    year = int(year)
    
    month_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12}
    
    month = month_dict[month]

    date = datetime.datetime(year, month, day, hour, minutes)
    return date

def clearList(liste) :
    if len(liste) > 10 :
        liste = liste[:10]
        return liste

class Not10Tweets(Exception) :
    def __init__(self, message) :
        self.message = message
    def __str__(self) :
        return self.message