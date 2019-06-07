from prediction import predict_by_vote
from tree import build_tree
from groups import create_bootstrap_group, create_test_group
#budowanie lasu
def build_forrest(data , max_depth, min_size, n_attributes, n_trees, n_tests, bg_size):
    forrest = list()
    score = int()
    print('trees',n_trees)
    for i in range(n_trees):
        i_train = create_bootstrap_group(data,bg_size)
        i_tree = build_tree(i_train, max_depth,min_size,n_attributes)
        forrest.append(i_tree)
        print('nr drzewa',i)
        i_test = create_test_group(data, n_tests)
        for j in range(len(i_test)):
            print('n test',j, i_test[j])
            prediction = predict_by_vote(forrest, i_test[j])
            [data, verification] = verify(data, prediction, i_test[j])
            score +=verification
    print(score)
    accuracy = score/n_trees/n_tests
    return accuracy

def verify(data, prediction, test):
    if( prediction == test["actual_classification"]):
        verification = 1
    else:
        print('test', test)
        verification = 0
        data.remove(test)
        test["probability"] = int(test["probability"]+1)
        data.append(test)
    return data, verification