import pandas as pd
df = pd.read_csv('./CoNLL-2003/ner.csv')
df.head()

# Split labels based on whitespace and turn them into a list
labels = [i.split() for i in df['labels'].values.tolist()]

# Check how many labels are there in the dataset
unique_labels = set()

for lb in labels:
  [unique_labels.add(i) for i in lb if i not in unique_labels]
 
print(unique_labels)
# >>> {'B-tim', 'B-art', 'I-art', 'O', 'I-gpe', 'I-per', 'I-nat', 'I-geo', 'B-eve', 'B-org', 'B-gpe', 'I-eve', 'B-per', 'I-tim', 'B-nat', 'B-geo', 'I-org'}

# Map each label into its id representation and vice versa
labels_to_ids = {k: v for v, k in enumerate(sorted(unique_labels))}
ids_to_labels = {v: k for v, k in enumerate(sorted(unique_labels))}
print(labels_to_ids)
# >>> {'B-art': 0, 'B-eve': 1, 'B-geo': 2, 'B-gpe': 3, 'B-nat': 4, 'B-org': 5, 'B-per': 6, 'B-tim': 7, 'I-art': 8, 'I-eve': 9, 'I-geo': 10, 'I-gpe': 11, 'I-nat': 12, 'I-org': 13, 'I-per': 14, 'I-tim': 15, 'O': 16}
