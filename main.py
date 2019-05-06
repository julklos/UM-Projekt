import numpy as np
import random

#tworzenie słownika- elementu drzewa
def create_dict(row):
    element = dict()
    element['probability'] = 1
    element['actual_classification'] = row[-1]
    row.pop()
    element['attributes'] = {i:x for i,x in enumerate(row)}
    return element

#pobieranie danych z pliku i wstępne ich przetwarzanie 
def read_file(filename):

    with open(filename, 'r') as f:
        data = f.readlines()

    dataset = list()

    for line in data:
        row = line.split()
        dataset.append(create_dict(row))
    return dataset

 #losowanie ze zbioru uczącego (dataset) pewnego pozbioru przypadków (grupa bootstrapowa) o rozmiarze bg_size
 #z uwzględnieniem, że elementy, dla których algorytm się do tej pory mylił (probability jest większe)
 #mają odpowiednio większą szansę na wylosowanie
def create_bootstrap_group(dataset, bg_size):
    indexes_to_sample = []

    for element in dataset:

        for _ in range(element['probability']):

            indexes_to_sample.append(dataset.index(element))

    chosen_indexes = random.sample(set(indexes_to_sample), bg_size)
    chosen_data = []

    for i in chosen_indexes:

        chosen_data.append(dataset[i])
    return chosen_data
#losowanie k atrybutów - attributes= len(attributes)
def draw_attriubutes(attributes, k):
    chosen_attributes = random.sample(range(attributes), k)
    return chosen_attributes
#wybór najlepszego podziału za pomocą indeksu zysku informacyjnego   
def get_best_split(dataset, attributes):
    entropy_parent = entropy_parent(dataset)
    for attribute in attributes:

#wyliczenie entropii poszczególnych dzieci       
def entropy_children(dataset):

#wyliczenie entropii rodzica- klasyfikacja dobry klient-zły klient
def entropy_parent(dataset):
    N = len(dataset)
    good = filter(lambda element: element['actual_classification'] == 1, dataset)
    p_good = len(good)/N
    p_bad = 1-p_good
    entropy = (-p_good*np.log2(p_good))+(-p_bad*np.log2(p_bad))
    return entropy

print('Hello UM')
data = read_file('german.data')
chosen_data = create_bootstrap_group(data,3)
print(draw_attriubutes(len(chosen_data[0]['attributes']),3))