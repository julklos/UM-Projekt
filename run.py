from forrest import build_forrest
from data import *
from groups import *
from tree import *

print('Hello UM')
data = read_file('german.data')
print(len(data))
print(build_forrest(data , 3, 2, 2,2, 3, 10))
