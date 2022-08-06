import numpy as np

import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download("maxent_ne_chunker")
# nltk.download("words")
# nltk.download("wordnet")

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

print("hello world")

tweet = "He broke into song as the buildings in Queen Street collapsed around him and the 100 sheep died."

words = word_tokenize(tweet)

lemmatizer = WordNetLemmatizer()

lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

print(lemmatized_words)

tagged = nltk.pos_tag(words)

print(tagged)


words_in_tweet = word_tokenize(tweet)
tweet_pos_tags = nltk.pos_tag(words_in_tweet)



# grammar = "NP: {<DT>?<JJ>*<NN>}"

# grammar = """
# Chunk: {<.*>+}
#        }<JJ>{"""

# chunk_parser = nltk.RegexpParser(grammar)

# tree = chunk_parser.parse(lotr_pos_tags)

tree = nltk.ne_chunk(tweet_pos_tags)

tree.draw()