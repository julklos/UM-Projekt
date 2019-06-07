import random
 #losowanie ze zbioru uczącego (dataset) pewnego pozbioru przypadków (grupa bootstrapowa) o rozmiarze bg_size
 #z uwzględnieniem, że elementy, dla których algorytm się do tej pory mylił (probability jest większe)
 #mają odpowiednio większą szansę na wylosowanie
def create_bootstrap_group(dataset, bg_size):
    indexes_to_sample = []

    for element in dataset:
        prob = element['probability']
        for _ in range(prob):
            indexes_to_sample.append(dataset.index(element))
    chosen_indexes = random.sample((indexes_to_sample), bg_size)
    chosen_data = []

    for i in chosen_indexes:

        chosen_data.append(dataset[i])
    return chosen_data

#losowanie grupy testowej- n elementów z całego zestawu danych- brak potrzeby powtórzeń
def create_test_group(data, n_tests):
    return random.sample(data, n_tests)

#losowanie k atrybutów - attributes= len(attributes)
def draw_attriubutes(attributes, k):
    chosen_attributes = random.sample(range(attributes), k)
    return chosen_attributes