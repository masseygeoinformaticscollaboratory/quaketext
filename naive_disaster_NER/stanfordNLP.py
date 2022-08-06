import stanza
# stanza.download('en') # download English model
# nlp = stanza.Pipeline('en') # initialize English neural pipeline
# doc = nlp("Barack Obama was born in Hawaii.") # run annotation over a sentence

nlp = stanza.Pipeline(lang='en', processors='tokenize', tokenize_no_ssplit=True)
doc = nlp("He broke into song as the buildings in Queen Street collapsed around him and the 100 sheep died.")

# print(doc)
# print(doc.entities) # this prints out all the words that were triggered by NER

for i, sentence in enumerate(doc.sentences):
    print(f'====== Sentence {i+1} tokens =======')
    print(*[f'id: {token.id}\ttext: {token.text}' for token in sentence.tokens], sep='\n')