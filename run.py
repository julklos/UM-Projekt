import numpy as np
import random

#pierwszy obiekt z set- ta implementacja nie ma złożoności zależnej od rozmiaru set
def get_first_object_from_set(set):
    for e in set:
        break
    return e
#tworzenie słownika- elementu drzewa
def create_dict(row):
    element = dict()
    element['probability'] = 1
    element['actual_classification'] = int(row[-1],10)
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
    max_information_gain = 0
    best_split = dict()
    best_split["terminal"] = dataset
    describition = "terminal"
    parent_entropy = entropy_classifier(dataset)
    for attribute in attributes:
        element = conditional_entropy(dataset, attribute)
        information_gain = parent_entropy - element['entropy']
        if(information_gain > max_information_gain):
            max_information_gain = information_gain
            best_split = element['split']
            describition = element['description']
    return {'split': best_split, 'description': describition}


#wyliczenie entropii warunkowej- pod warunkiem danego podziału    
def conditional_entropy(dataset, attribute):
    values = set()
    for data in dataset:
        values.add(data['attributes'][attribute])
    if(get_first_object_from_set(values)[0]=='A'):
     
        return conditional_entropy_categorical(dataset,attribute,values)
    else:
    
        return conditional_entropy_numerical(dataset, attribute, values)

#entropia warunkowa dla danych kategorycznych
def conditional_entropy_categorical(dataset, attribute,values):
    N = len(dataset)
    entropy = 0
    split = dict()
    for value in values:
        filtered = list(filter(lambda element: element['attributes'][attribute] == value,dataset))
        filtered_len = len(filtered)
        entropy += filtered_len/N*entropy_classifier(filtered)
        split[value] = filtered
    return {'split': split, 'entropy': entropy, 'description': {'attribute': attribute , 'value': values}}

#entropia warunkowa dla danych numerycznych
def conditional_entropy_numerical(dataset,attribute, values):
    N = len(dataset)
    best_entropy = 1000
    split = dict()
    split["terminal"]= dataset
    for value in values:
        left, right = list(), list()
        left = list(filter(lambda element: element['attributes'][attribute] <= value,dataset))
        right = list(filter(lambda element: element['attributes'][attribute] > value,dataset))
        entropy = len(left)/N*entropy_classifier(left)+len(right)/N*entropy_classifier(right)
        if( entropy < best_entropy):
            best_entropy = entropy
            split['left'] = left
            split['right'] = right
            split.pop("terminal",None)
            b_value = value
    return {'split': split, 'entropy': best_entropy, 'description': {'attribute': attribute , 'value': b_value}}

        

#wyliczenie entropii rodzica- klasyfikacja dobry klient-zły klient
def entropy_classifier(dataset):
    N = len(dataset)
    good = list(filter(lambda element: element['actual_classification'] == 1, dataset))
    if(len(good) in [N, 0] ):
        entropy = 0
    else:
        p_good = len(good)/N
        p_bad = 1-p_good
        entropy = (-p_good*np.log2(p_good))+(-p_bad*np.log2(p_bad))
    return entropy

#ustawianie koncowego elementu
def set_terminal(last_node):
    good=len(list(filter(lambda element: element['actual_classification'] == 1, last_node )))
    bad =len(list(filter(lambda element: element['actual_classification'] == 2, last_node )))
    if good > bad:
        return 1
    else:
        return 2
#podział 
def split(node, max_depth, min_size, n_attributes, depth):
    print('node', node)
    #sprawdzenie czy dalszy podział ma sens
    keys = list(node.keys())
    if(len(keys) == 1):
        print('keys = 1')
        node["description"] = set_terminal(node["terminal"])
        return
    #jeśli jest zbyt głębokie drzewo- koniec
    print(depth)
    if(depth == max_depth):
        print('max depth')
        for key in keys:
            new_key = dict()
            terminal = dict()
            terminal["terminal"] = node[key]
            new_key["split"] = terminal
            new_key["description"] = set_terminal(new_key["split"]["terminal"])
            node[key]=new_key
        return
    else:
        print('go on')
        for key in keys:
            attributes = draw_attriubutes(len(node[key][0]['attributes']),n_attributes)
            node[key]= get_best_split(node[key],attributes)
            split(node[key]['split'], min_size, max_depth, n_attributes, depth+1)
            
 
#budowanie pojedynczego drzewa
def build_tree(train, max_depth, min_size, n_attributes):
    attributes = draw_attriubutes(len(train[0]['attributes']),n_attributes)
    root = get_best_split(train, attributes)
    split(root['split'], max_depth, min_size, n_attributes, 1)
    return root
#budowanie lasu
def build_forrest(data , max_depth, min_size, n_attributes, n_trees, n_tests, n_group):
    forrest = list()
    for i in range(n_trees):
        i_train = create_bootstrap_group(data,n_group)
        i_tree = build_tree(i_train, max_depth,min_size,n_attributes)
        forrest.append(i_tree)
        i_test = create_test_group(data, n_tests)
        for j in range(i_test):
            #prediction = predict_by_vote(forrest, i_test[j])
            [data, verification] = verify(data, prediction, i_test)



#def predict():
#def predict_by_vote(forrest, test):
#losowanie grupy testowej- n elementów z całego zestawu danych- brak potrzeby powtórzeń
def create_test_group(data, n_tests):
    return random.sample(data, n_tests)
def verify(data, prediction, test):
    if( prediction == test[0]["actual_classification"]):
        print('its OK')
        verification = 1
    else:
        print('its not OK')
        verification = 0
        data.remove(test[0])
        test[0]["probability"] = test[0]["probability"]+1
        data.append(test)
    return data, verification
print('Hello UM')
data = read_file('german.data')
chosen_data = create_bootstrap_group(data,3)
#attributes = draw_attriubutes(len(chosen_data[0]['attributes']),4)
#print(get_best_split(chosen_data,attributes ))
#print(build_tree(chosen_data, 5,3,2))
chosen_element = create_bootstrap_group(chosen_data,1)
print('group', chosen_data)
print('element', chosen_element)
print('new group', verify(chosen_data,1,chosen_element))