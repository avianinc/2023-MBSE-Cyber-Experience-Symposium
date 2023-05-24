import json
from anytree import Node, RenderTree

# Load the JSON object into a Python dictionary
with open('./examples/data/elements.json', 'r') as f:
    data = json.load(f)


keyID = 'eb5e8993-bc67-425a-9b58-ad39bd9cf621'
keyInstance = data[keyID]['data'][1]['kerml:esiData']['instance']['@id']

print(keyInstance)

instanceID = keyInstance
instanceName = data[instanceID]['data'][1]['kerml:name']

print(instanceName)