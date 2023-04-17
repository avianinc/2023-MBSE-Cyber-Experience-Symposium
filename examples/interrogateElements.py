import json
from anytree import Node, RenderTree

# Load the JSON object into a Python dictionary
with open('./examples/elements.json', 'r') as f:
    data = json.load(f)

#list the keys
#for keys in data:
    #print(keys)

keyID = '7d73925a-f5af-4d8f-8b04-0a3985b21409'
keyName = data[keyID]['data'][1]['kerml:name']
keyOwnedElements = data[keyID]['data'][1]['kerml:ownedElement']

print(keyName, keyOwnedElements)


