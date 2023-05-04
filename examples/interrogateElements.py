# Some test code to interrogate the elements.json file

import json
from anytree import Node, RenderTree

# Load the JSON object into a Python dictionary
with open('./examples/data/test_elements.json', 'r') as f:
    data = json.load(f)

#list the keys
#for keys in data:
    #print(keys)

# Pick a key with an owned element and look at the data
keyID = '7d73925a-f5af-4d8f-8b04-0a3985b21409'
keyName = data[keyID]['data'][1]['kerml:name']
keyOwnedElements = data[keyID]['data'][1]['kerml:ownedElement']
print(keyName, keyOwnedElements)

# Pick a key with a value and look at the data
keyID = '51d7d3b3-3d47-42c0-91fd-1fb051630901'
keyName = data[keyID]['data'][1]['kerml:name']
keyType = data[keyID]['data'][0]['@type'][1]
keyValue = data[keyID]['data'][1]['kerml:esiData']['value']
print(keyName, keyType, keyValue)

# Lets go though InstanceSpecification
keyID = 'd5fd2074-9daf-4f70-a441-53e52eed36d7'
keyType = data[keyID]['data'][0]['@type'][1]
print(keyType)

# get slot name
# do this by getting the keyID of the slot
# then get the slot name of the slot from the ['data'][1]['kerml:name']
keyID = 'c0fcd17b-8e49-402a-bf51-41a79f01012e'
keyType = data[keyID]['data'][0]['@type'][1]
slotDefiningFeature = data[keyID]['data'][1]['kerml:esiData']['definingFeature']['@id']
slotNameFromDefiningFEature = data[slotDefiningFeature]['data'][1]['kerml:name']

print(keyType, slotDefiningFeature, slotNameFromDefiningFEature)