import spacy

from spacy import displacy

nlp = spacy.load("./output/model-last/") #load the model

text = "#QUETTA: At least 421 people have been killed, 21 thousand houses affected due to #earthquake in Balochistan, Chairman NDMA says."

doc = nlp(text)
print(nlp.pipe_names)

displacy.serve(doc, style="ent")