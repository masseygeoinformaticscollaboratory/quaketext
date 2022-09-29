import spacy
from spacy import displacy

NER=spacy.load('en_core_web_sm')

raw_text="BREAKING: A 7.8-magnitude earthquake struck off Chile's northern coast Wednesday night, triggering a tsunami... http://t.co/WRbyO79to2"

text1= NER(raw_text)

for word in text1.ents:
    print(word.text,word.label_)