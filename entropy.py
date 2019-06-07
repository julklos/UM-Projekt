import numpy as np
#pierwszy obiekt z set- ta implementacja nie ma złożoności zależnej od rozmiaru set
def get_first_object_from_set(set):
    for e in set:
        break
    return e

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
    #klasyfikowanie gdyby okazało się, że dane testowe zawierają inną wartość atrybutu niż te z dataset
    classify = set_terminal(dataset)
    for value in values:
        filtered = list(filter(lambda element: element['attributes'][attribute] == value,dataset))
        filtered_len = len(filtered)
        entropy += filtered_len/N*entropy_classifier(filtered)
        split[value] = filtered
    
    return {'split': split, 'entropy': entropy, 'description': {'attribute': attribute , 'value': values, 'actual_node_classification': classify}}

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