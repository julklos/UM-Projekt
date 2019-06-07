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