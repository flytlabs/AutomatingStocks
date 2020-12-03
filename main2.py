import tweepy
def getTweets(userID, amnt):

    consumer_key = "7Oc83swm0SOz3GTEwqWaVWxlg"
    consumer_secret = "skqeAT7r21t9OH8iq0TsdmdrnUqMCbL1bg5dnzig5NG9NlhyuS"
    access_token = "1274527723965288448-DNSJFc10vsHn7HyNDVxhGVRWONl97m"
    access_token_secret = "qxoLpMlVeCsmLMzTwSlkvBGN7Al3zWLr2gqzi0GMLtyb3"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # get tweets
    tweets = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=amnt,
                               include_rts=False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )
    sortedtweets = []

    # extract tweets from objects
    for tweet in tweets:
        text = tweet.full_text
        sortedtweets.append(text)

    return sortedtweets

def findTickers(tweets):
    tickers = []
    utickers = []

    # find tickers -> extract from $ to next white space
    for tweet in tweets:
        if "$" in tweet:
            ticker = tweet[tweet.find("$") + 1:].split()[0]
            tickers.append(ticker.lower())

    # cleaning algorithm
    for elem in tickers:
        try:
            int(elem)
        except:
            if not "$" or "," or "k"  in elem:
                if len(elem) <= 4:
                    utickers.append(elem)

    return utickers

def countTickers(tickers):

    dict = {}

    # count
    for ticker in tickers:
        if ticker in dict.keys():
            dict[ticker] = dict[ticker] + 1
        else:
            dict[ticker] = 1

    return dict

# runtime
nlist = ['RadioSilentPlay', 'SuperDuperInvst', 'AlexDelarge6553', 'MikeKnowsRunner', 'StockHighArmy']

# special list
slist = []

for user in nlist:
    tickers = findTickers(getTweets(user, 500))
    tickerdict = countTickers(tickers)
    for ticker,num in tickerdict.items():
        if num <= 2 and ticker not in tickers[10:]:
            slist.append(ticker)


finallist = []

for ticker in slist:
    finallist.append(ticker + ' - ' + str(slist.count(ticker)))
    print(ticker)

# do more with final list here (sentiment analysis etc?)

