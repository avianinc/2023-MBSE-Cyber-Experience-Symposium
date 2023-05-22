import json

filename = './examples/elements_latest.json'

with open(filename, 'r') as file:
    data_string = file.read()

data = json.loads(data_string)
sysml_uuid = '9c8ab8a4-25a1-40f5-909c-15264d7bae33'
sysml_element = data[sysml_uuid]["data"][1]

def display_element(element):
    print("Element Name:", element["kerml:name"])
    print("Element Type:", element["@type"])
    print("Element ID:", element["@id"])
    print("Element Modified Time:", element["kerml:modifiedTime"])
    print("\nOwned Elements:")
    for owned_element in element["kerml:ownedElement"]:
        print("  - Element ID:", owned_element["@id"])

def explore_element(element, owned_element_id):
    for owned_element in element["kerml:esiData"]["_instanceValueOfInstance"]:
        if owned_element["@id"] == owned_element_id:
            print(json.dumps(owned_element, indent=2))
            if "Value" in owned_element:
                print("\nesiData:")
                print(json.dumps(element["kerml:esiData"], indent=2))
            break

display_element(sysml_element)

while True:
    print("\nEnter 'q' to quit or an Owned Element ID to explore:")
    choice = input().strip()
    if choice == 'q':
        break
    else:
        explore_element(sysml_element, choice)
