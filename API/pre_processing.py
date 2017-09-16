import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
import string


def process_corpus(content, pos_tags, question):
    stop_words = stopwords.words('english')
    punctuation_list = [unicode(i) for i in string.punctuation]
    for punctuation in punctuation_list:
        stop_words.append(punctuation)

    # split three categories: 1 no improvemnt 2 with pos_tags words 3 others
    doc_noimprove = []
    doc_nn = []
    nn_extracted = []
    doc_other = []
    for review in content:
        if 'no improvement' in review:
            doc_noimprove.append(review)
        else:
            nn_list = []
            sen = review
            pos_new = nltk.pos_tag(nltk.word_tokenize(sen))
            for token in pos_new:
                if token[1] in pos_tags and not token[0] in stop_words:
                    nn_list.append(token[0])
            # stemming
            stemmer = PorterStemmer()
            for counter, word in enumerate(nn_list):
                nn_list[counter] = stemmer.stem(word)
            # apply rule
            switcher = {
                1: rule_q1, 2: rule_q2, 3: rule_q3, 4: rule_q4, 5: rule_q5, 6: rule_q6,
                7: rule_q7, 8: rule_q8, 9: rule_q9, 10: rule_q10
            }
            # Get the function from switcher dictionary to process corresponding question
            func = switcher.get(question, lambda: "Question number must between 1-10 (inclusive)!")
            # Execute the function
            nn_list = func(sen, nn_list)

            if nn_list != []:
                nn_extracted.append(nn_list)
                doc_nn.append(sen)
            else:
                doc_other.append(sen)
    return doc_noimprove, [doc_nn, nn_extracted], doc_other


def rule_q1(sen, ne):
    clean_ne = list(set(ne))
    #     remove_words = ["improv", "custom", "servic", "peopl","person","facil","avail","good",\
    #                     "center","centr","car", "dealership", "vehicl", "toyota", "problem","work", "much",\
    #                    "thing", "possibl","need"]   #stemmed
    remove_words = ['custom', 'car', 'vehicl', 'servic', 'toyota', 'thing', 'good', \
                    'day', 'center', 'centre', 'dealership', 'time']
    clean_ne = [word for word in clean_ne if word not in remove_words]

    save_words = ['inform', 'tell', 'advis', 'understand', 'advic', 'call', 'answer', 'correct', 'guid', \
                  'train', 'suggest', 'respons', 'commit', 'solv', 'queri', 'updat', 'attend', 'deliv', \
                  'wait', 'mention', 'listen', 'resolv', 'respond', 'share', 'commun', 'confirm', \
                  'behavior', 'behav', 'properly', 'proper']  # stemmed
    clean_ne = clean_ne + [stemmer.stem(word) for word in sen.split() if stemmer.stem(word) in save_words]
    clean_ne = list(set(clean_ne))

    # rules to merge keywords:
    if 'share' in clean_ne:
        clean_ne[clean_ne.index('share')] = 'inform'
    if 'tell' in clean_ne:
        clean_ne[clean_ne.index('tell')] = 'inform'
    if 'behav' in clean_ne:
        clean_ne[clean_ne.index('behav')] = 'behavior'
    if 'advic' in clean_ne:
        clean_ne[clean_ne.index('advic')] = 'advis'
    if 'queri' in clean_ne:
        clean_ne[clean_ne.index('queri')] = 'question'
    if 'properly' in clean_ne:
        clean_ne[clean_ne.index('properly')] = 'proper'
    if 'worker' in clean_ne:
        clean_ne[clean_ne.index('worker')] = 'staff'

    # rules to split keywords:
    if 'inform' in clean_ne and 'information' in sen:
        clean_ne[clean_ne.index('inform')] = 'information'
    if 'respons' in clean_ne:
        if ('responsibility' in sen or 'responsibilities' in sen or 'responsible' in sen):
            clean_ne[clean_ne.index('respons')] = 'responsibility'
        else:
            clean_ne[clean_ne.index('respons')] = 'respond'
    if 'listen' in clean_ne:
        clean_ne[clean_ne.index('listen')] = 'respond'

    clean_ne = list(set(clean_ne))
    return clean_ne