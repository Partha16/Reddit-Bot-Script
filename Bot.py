import praw
from googletrans import Translator
from PyDictionary import PyDictionary
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 9

reddit = praw.Reddit(client_id='_4Btkc-hzv-mJA',
                     client_secret='uRntAJw5QeGtqnvTbUdU5Gomd2Y',
                     username='i_am_stupid_bot',
                     password='9942157145',
                     user_agent='hi')

subreddit = reddit.subreddit('dsproject')
keyword = '!translate'
keyword1 = '!meaning'
keyword2 = '!tldr'
end = '\n\n_____________________________________________\n^^Beep ^^bop ^^Im ^^a ^^bot  ^^If ^^you ^^have ^^a ^^problem ^^contact ^^/u/hate_mi '
translator = Translator()

l1 = []
l2 = []
l3 = []

dictionary = PyDictionary()

badwebs = ['youtube','imgur','republictv']

def summarizer(url):
    for x in badwebs:
        if x in url:
            return 'Not used for this website.'
    try:
        summary = 'The summary of the Article.\n>'
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summary = summary + '\n' + str(sentence)
        return summary
    except:
        return 'No summary could be created.'

def clearer(l):
    if len(l)>200:
        l = []

def translate(parent,comment):
    try:
        return(translator.translate(parent.body,dest=k[1]).text)
    except:
        try:
            return(translator.translate(parent.text,dest=k[1]).text)
        except:
            try:
                return(translator.translate(parent.title,dest=k[1]).text)
            except:
                return('Translating language not identified.')
    l1.append(comment.id)
    clearer(l1)
   
def meaning(comment):
    try:
        parent = comment.parent()
        comment.reply(dictionary.meaning(parent.body) + end)
    except:
        comment.reply('Not a meaningful word.' + end)
    l2.append(comment.id)
    clearer(l2)

#main function  
   
end = str(end)
for comment in subreddit.stream.comments(skip_existing=True ):
    print(comment.body)
    word = comment.body
    k = word.split(' ')
    
    if len(k) == 1:
        k.append('english')
        
    if keyword in comment.body:
        try:
            if comment.id not in l1:
                k[1] = k[1].lower()
                parent = comment.parent()
                comment.reply(translate(parent,comment) + end)
        except:
            comment.reply('Translating language not identified.' + end)
            
    elif keyword1 in comment.body:
        if comment.id not in l2:
            meaning(comment)
            
    elif keyword2 in comment.body:
        if comment.id not in l3:
            parent = comment.parent()
            try:
                comment.reply(summarizer(parent.url) + end)
            except:
                try:
                    if '(' in parent.body:
                        s = parent.body
                        start = s.find("(") + len("(")
                        en = s.find(")")
                        url = s[start:en]
                        print(url)
                        comment.reply(summarizer(url) + end)
                    else:    
                        comment.reply(summarizer(parent.body) + end)
                except:
                    comment.reply('None to be summarized.' + str(end))
            print('*****************************')
            l3.append(comment.id)
            clearer(l3)
