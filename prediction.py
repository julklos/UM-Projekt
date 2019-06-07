def predict(tree, test):
    #czy nie jest to ostatni element - pobierz przewidywaną klasyfikację
    if 'terminal' in tree:
        return  tree['description']
    elif 'terminal' in tree['split']:
        prediction = tree['split']['description']
        return prediction
        #czy descripton.value jest length == 1
        # jest tak to porównaj czy wartosc testu jet wieksza czy mniejsza i jedzim dalej
    else:
        attribute = tree['description']['attribute']
        if type(tree['description']['value']) is set :
            #  jesli nie jest wywołaj podział od wartosc atrybutu, ktora ma test..
            test_value = test['attributes'][attribute]
            #sprawdz czy dana testowa ma wartosc atrybutu ktora byla brana pod uwage przy podziale drzewa
            if test_value in tree['description']['value']:
                return predict(tree['split'][test_value],test)
            else:
                prediction = tree['description']['actual_node_classification']
                return prediction
        else:
            value = tree['description']['value']
            if(test['attributes'][attribute]> value):
                return predict(tree['split']['right'], test) 
            else:
                return predict(tree['split']['left'], test)

    #czy descripton.value jest length == 1
     # jest tak to porównaj czy wartosc testu jet wieksza czy mniejsza i jedzim dalej
    # jesli nie jest wywołaj podział od wartosc atrybutu, ktora ma test..
    
def predict_by_vote(forrest, test):
    result = list()
    for tree in forrest:
        res = predict(tree, test)
        result.append(res)

    good=len(list(filter(lambda element: element == 1, result )))
    bad =len(list(filter(lambda element: element == 2, result )))
    if good > bad :
        return 1
    else:
        return 2

