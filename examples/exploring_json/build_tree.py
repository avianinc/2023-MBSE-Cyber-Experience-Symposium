import json
from anytree import Node, RenderTree

def build_tree(data, keyID, parent=None):
    key_data = data[keyID]['data'][1]
    keyOwnedElements = key_data['kerml:ownedElement']

    node = Node(keyID, parent=parent)

    for element in keyOwnedElements:
        child_keyID = element["@id"].replace("#", "")
        build_tree(data, child_keyID, parent=node)

    return node

# Replace 'elements.json' with the path to your JSON file
with open('elements.json', 'r') as f:
    data = json.load(f)

starting_keyID = '7d73925a-f5af-4d8f-8b04-0a3985b21409'
tree = build_tree(data, starting_keyID)

for pre, _, node in RenderTree(tree):
    print(f"{pre}{node.name}")
