import tweepy
import emoji
import time
import random
import threading

#==================================SETUP=============================================

#Keys for api
CONSUMER_KEY = 'luDRvBJAG0fKJnd20eoef9xCW'
CONSUMER_SECRET = 'nWEuwcUiyEceFPa1CCnh8s598fS9RbOYTYKx5LbMOSakAq9qpw'
ACCESS_KEY = '1161961422051524609-8jqgUBwELyc9eigHbviOjxoNaan34a'
ACCESS_SECRET = 'UGek5bE9K7u7CNSk3ZxxghJx7f3zfyoOULaPuoI9VTenB'

#Setup api object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#store name of last seen id
FILENAME = 'last_seen_id.txt'

#==================================METHODS=============================================

#get banana vocab from file
def get_banana_vocab():
    #Store vocab in a global list
    f_read = open('bananaVocab.txt', 'r')
    banana_vocab = f_read.read().strip().split(',')
    f_read.close()
    return banana_vocab

#Generates joke of specified word length
def generate_joke(length):
    BANANA_VOCAB = get_banana_vocab()
    joke_words = []

    #Put some random words from vocab into jokes in random order
    for i in range(length):
        joke_words.append(BANANA_VOCAB[random.randint(0, len(BANANA_VOCAB)-1)])

    #Ensure atleast one of the words is "banana"
    joke_words[random.randint(0,len(joke_words)-1)] = "banana"

    #convert list into string
    joke = ' '.join(joke_words) + '!'

    return joke

#Retrieve last seen id from last seen id txt file
def retrieve_last_id(fileName):
    f_read = open(fileName, 'r')
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id

#store last seen id in last seen id txt file
def store_last_id(last_id, fileName):
    f_write = open(fileName, 'w')
    f_write.write(str(last_id))
    f_write.close()
    return

def reply_to_mentions():
    print('checking for mentions and replying...')
    #Get new mentions from last seen mention using last seen id
    last_id = retrieve_last_id(FILENAME)
    mentions = api.mentions_timeline(last_id, tweet_mode='extended')

    #From these reply appropriately
    for mention in reversed(mentions):

        #Notify terminal which tweet we're looking at
        print(str(mention.id) + ' | ' + mention.full_text)

        #update last seen id
        last_id = mention.id
        store_last_id(last_id, FILENAME)

        #Reply to the tweet
        print('Responding to tweet!')
        api.update_status('@' + mention.user.screen_name + emoji.emojize(":orangutan:"), mention.id)

def tweet_banana_joke():
    joke = generate_joke(random.randint(4, 9))

    print("Tweeting joke: " + joke)
    api.update_status(joke)

def tweet_banana_joke_thread():

    print("============Thread Status============")
    print("")
    print("Active Threads: ", threading.activeCount())
    print("Thread Objects: ", threading.enumerate())
    print("")
    print("====================================")
    #make the tweet then wait an hour
    tweet_banana_joke()
    time.sleep(3605)

    #call itself
    tweet_banana_joke_thread()


def reply_to_mentions_thread():

    #Check and reply to mentions then wait 30 seconds
    reply_to_mentions()
    time.sleep(30)

    #call itself
    reply_to_mentions_thread()

#==================================MAIN=============================================

t1 = threading.Thread(target = tweet_banana_joke_thread, args = ())
t2 = threading.Thread(target = reply_to_mentions_thread, args = ())

t1.start()
t2.start()
