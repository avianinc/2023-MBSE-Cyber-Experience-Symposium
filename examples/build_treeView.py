import tkinter as tk
from tkinter import ttk
from anytree import Node, RenderTree
import json

# Load the JSON object into a Python dictionary
with open('elements.json', 'r') as f:
    data = json.load(f)

# The function to create the tree structure
def create_tree(node_id):
    node_name = node_id
    node = Node(node_name)

    owned_elements = data[node_id]['data'][1]['kerml:ownedElement']
    for owned_element in owned_elements:
        element_id = owned_element['@id']
        child_node = create_tree(element_id)
        child_node.parent = node

    return node

# The function to insert nodes into the Treeview
def insert_treeview_nodes(treeview, parent, tree_node):
    treeview_node = treeview.insert(parent, 'end', text=tree_node.name)

    for child in tree_node.children:
        insert_treeview_nodes(treeview, treeview_node, child)

    # Set the node to the open state
    treeview.item(treeview_node, open=True)

def on_treeview_select(event):
    item_id = tree.item(tree.focus())['text']
    if item_id in data:
        json_data = data[item_id]
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(json_data, indent=2))
    else:
        text_area.delete(1.0, tk.END)

root = tk.Tk()
root.geometry("800x600")

paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

frame1 = ttk.Frame(paned_window)
paned_window.add(frame1, weight=1)

frame2 = ttk.Frame(paned_window)
paned_window.add(frame2, weight=1)

tree = ttk.Treeview(frame1)
tree.pack(fill=tk.BOTH, expand=True)

text_area = tk.Text(frame2, wrap=tk.WORD)
text_area.pack(fill=tk.BOTH, expand=True)

root_node_id = '7d73925a-f5af-4d8f-8b04-0a3985b21409'  # Replace with the desired root node ID
root_node = create_tree(root_node_id)
insert_treeview_nodes(tree, '', root_node)

tree.bind('<<TreeviewSelect>>', on_treeview_select)

root.mainloop()
