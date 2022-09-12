import stanza
# stanza.download('en') # download English model
# nlp = stanza.Pipeline('en') # initialize English neural pipeline
# doc = nlp("Barack Obama was born in Hawaii.") # run annotation over a sentence

nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt, pos, lemma, ner', tokenize_no_ssplit=True)
# need to specify what processors to use in order to analyze the text

# doc = nlp("He broke into song as the buildings in Queen Street collapsed around him and the 100 sheep died.")

doc = nlp("Chris Manning teaches at Massey University. He lives in the Green Bay Area, only 10 minutes from Albany.")


# print(doc)
print(doc.entities) # this prints out all the words that were triggered by NER

disasterNERlist = ["break", "collapse", "lost", "kill", "die"]

for i, sentence in enumerate(doc.sentences):
    print(f'====== Sentence words =======')
    print(*[f'word: {word.text}\tlemma: {word.lemma}' for word in sentence.words], sep='\n')
    print(f'====== Sentence ents =======')
    print(*[f'ent: {ent.text}\ttype: {ent.type}' for ent in sentence.ents], sep='\n')
    print(f'====== Sentence tokens =======')
    print(*[f'token: {token.text}\tner: {token.ner}' for token in sentence.tokens], sep='\n')