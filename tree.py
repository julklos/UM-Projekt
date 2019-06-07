from entropy import entropy_classifier, conditional_entropy, set_terminal
from groups import draw_attriubutes

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


#podział 
def split(node, max_depth, min_size, n_attributes, depth):
    #sprawdzenie czy dalszy podział ma sens
    keys = list(node.keys())
    if(len(keys) == 1):
        node["description"] = set_terminal(node["terminal"])
        return
    #jeśli jest zbyt głębokie drzewo- koniec
    elif depth == max_depth:
        for key in keys:
            terminal = dict()
            terminal["terminal"] = node[key]
            terminal["description"] = set_terminal(terminal["terminal"])
            node[key]=terminal
        return
    else:
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