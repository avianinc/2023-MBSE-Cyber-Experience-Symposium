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

keyID = '51d7d3b3-3d47-42c0-91fd-1fb051630901'
keyName = data[keyID]['data'][1]['kerml:name']
keyType = data[keyID]['data'][0]['@type'][1]
keyValue = data[keyID]['data'][1]['kerml:esiData']['value']

print(keyName, keyType, keyValue)




