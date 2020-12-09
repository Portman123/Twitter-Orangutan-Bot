import random

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

    return(generate_question() + '\n \n' + generate_short_statement())

for i in range(10):
    joke = generate_joke()
    print(joke)
    print('\n\n\n')
