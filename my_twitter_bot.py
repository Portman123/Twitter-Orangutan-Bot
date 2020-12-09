import tweepy
import emoji
import time
import random
import threading

#==================================SETUP=============================================
f_read = open('access_stuff.txt', 'r')
access = f_read.read().strip().split(',')

#Keys for api
CONSUMER_KEY = access[0]
CONSUMER_SECRET = access[1]
ACCESS_KEY = access[2]
ACCESS_SECRET = access[3]

#Setup api object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#store name of last seen id
FILENAME = 'last_seen_id.txt'

#==================================METHODS=============================================

#get banana vocab from file
def get_vocab(type):
    #Store vocab in a global list
    f_read = open(type, 'r')
    vocab = f_read.read().strip().split(',')
    f_read.close()
    return vocab

#Generates a simple (ofetn nonsensical) question
def generate_question():

    #get words from vocab bank
    interrogative_words = get_vocab('interrogative.txt')
    verbPast_words = get_vocab('verbPast.txt')
    article_words = get_vocab('article.txt')
    noun_words = get_vocab('noun.txt')

    #pick random words from the vocab banks
    interrogative = interrogative_words[random.randint(0, len(interrogative_words)-1)]
    verbPast = verbPast_words[random.randint(0, len(verbPast_words)-1)]
    article = article_words[random.randint(0, len(article_words)-1)]
    noun = noun_words[random.randint(0, len(noun_words)-1)]

    #form question
    question = [interrogative, verbPast, article, noun]

    #convert to string
    questionString = ' '.join(question) + '?'

    #output
    #print(questionString)
    return questionString

##Generates a simple (ofetn nonsensical) question
def generate_short_statement():

    #get words from vocab bank
    article_words = get_vocab('article.txt')
    intensifier_words = get_vocab('intensifier.txt')
    adjective_words = get_vocab('adjective.txt')
    noun_words = get_vocab('noun.txt')

    #pick random words from vocab banks
    article = article_words[random.randint(0, len(article_words)-1)]
    intensifier = intensifier_words[random.randint(0, len(intensifier_words)-1)]
    adjective = adjective_words[random.randint(0, len(adjective_words)-1)]
    noun = noun_words[random.randint(0, len(noun_words)-1)]

    #form statement
    statement = [article, intensifier, adjective, noun]

    #convert to string
    statementString = '...' + ' '.join(statement) + '!'

    #output
    #print(statementString)
    return statementString

def generate_joke():

    return(emoji.emojize(":orangutan:") + ' ' + generate_question() + '\n \n' + generate_short_statement() + ' ' + emoji.emojize(":banana:"))


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
    joke = generate_joke()

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
