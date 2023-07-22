## make sure to import nltk and the downloads listed below
### nltk.download('punkt')
### nltk.download('stopwords')
### nltk.download('wordnet')


import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import wordnet

def get_flashcards(text, num_keywords = 12):  ## passes the text #you can get the no.of keywords from the user input also 

    def get_clean_tokens(text):
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        clean_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
        return clean_tokens

    def get_keywords_with_definitions(text, num_keywords = 12):
        tokens = get_clean_tokens(text)
        freq_dist = FreqDist(tokens)
        keywords = freq_dist.most_common(num_keywords)

        flashcards = []
        for keyword, frequency in keywords:
            synsets = wordnet.synsets(keyword)
            if synsets:
                definition = synsets[0].definition()  
                flashcards.append((keyword, frequency, definition))
            else:
                flashcards.append((keyword, frequency, "No definition found."))

        return flashcards

    flashcards = get_keywords_with_definitions(text, num_keywords)

    # Save flashcards to a JSON file
    output_file = "Generatedflashcards.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(flashcards, json_file, ensure_ascii=False, indent=4)

    return flashcards



    ### code to recieve the flashcard from main
    #   get_flashcards = get_flashcards(text)

    ## recieve with the number of times teh word has appeared in text 
    ##  print("Keywords with Definitions with the no.of times it appeared in the text:")
    ##  for keyword, frequency, definition in extracted_keywords: 
    ##  print(f"{keyword}: {frequency} - Definition: {definition}")

     ## recieve without frequency
    ##  print("Keywords with Definitions with the no.of times it appeared in the text:")
    ##  for keyword, frequency, definition in extracted_keywords: 
    ##  print(f"{keyword}: {frequency} - Definition: {definition}")

