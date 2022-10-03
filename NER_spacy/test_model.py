import spacy

from spacy import displacy

nlp = spacy.load("./output/model-last/") #load the model

# text = "#QUETTA: At least 421 people have been killed, 21 thousand houses affected due to #earthquake in Balochistan, Chairman NDMA says."

# text = "Chile Earthquake: 5 Dead, Several Seriously Injured http://t.co/9v1Xr25bNg"

# text = "RT @TIME: See India's rescue operations in the villages most affected by Nepal's deadly earthquake http://t.co/Tcirp7hceR http://t.co/LCMDoâ€¦"

text = "Over 330 peoples are killed in #Earthquake in #Baluchistan. Many are still missing. #Pakistan"

doc = nlp(text)
print(nlp.pipe_names)

displacy.serve(doc, style="ent")