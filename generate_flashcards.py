import os
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import wordnet

def get_keywords_with_definitions(textfile, num_keywords=12):

    with open(os.getcwd() + "\\pickle_notes\\" + textfile + "_pickle", "rb") as fp:  # Unpickling
        text = pickle.load(fp)

    tokens = get_clean_tokens(text)
    freq_dist = FreqDist(tokens)
    keywords = freq_dist.most_common(num_keywords)

    flashcards = []
    for keyword, frequency in keywords:
        synsets = wordnet.synsets(keyword)
        if synsets:
            definition = synsets[0].definition()
            print(keyword)
            flashcards.append((keyword, frequency, definition))
        else:
            flashcards.append((keyword, frequency, "No definition found."))

    return flashcards

def get_clean_tokens(text):
    print(type(text))
    for i in range (len(text)):
        stringText =text[i] + " ";
    tokens = word_tokenize(stringText.lower())
    stop_words = set(stopwords.words('english'))
    clean_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return clean_tokens

