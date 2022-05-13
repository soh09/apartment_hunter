import sys
import json

with open(sys.path[0] + '/input.json', 'r') as j:
    inputs = json.load(j)


print(type(inputs))
print(inputs)