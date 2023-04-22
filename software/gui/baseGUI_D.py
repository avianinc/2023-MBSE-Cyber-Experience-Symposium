#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

TWC and Intsance interfacing demonstration: This tool demonstartes 
communicationswith Cameos Teamwork Cloud API and interrogating an 
instance. The instance can be reviewed and written to disk according 
to the needs of the simulation toolset.

Author: J.K. DeHart
Date: 3/2/2023
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from anytree import Node, RenderTree
import os
import requests
import json


class App:

    def __init__(self, master):
        self.master = master
        self.master.title("TWC API Interactions - Demo")
        self.master.geometry("800x600")

        # Server Info
        self.server_info_frame = tk.Frame(self.master, padx=10, pady=10)
        self.server_info_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(self.server_info_frame, text="Server Info").grid(row=0, column=0, sticky="w")
        tk.Label(self.server_info_frame, text="Server IP").grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(self.server_info_frame, text="Server Port").grid(row=2, column=0, sticky="w", pady=2)
        tk.Label(self.server_info_frame, text="Auth Key").grid(row=3, column=0, sticky="w", pady=2)
        self.server_ip_entry = tk.Entry(self.server_info_frame)
        self.server_ip_entry.grid(row=1, column=1, sticky="w", pady=2)
        self.server_port_entry = tk.Entry(self.server_info_frame)
        self.server_port_entry.grid(row=2, column=1, sticky="w", pady=2)
        self.auth_key_entry = tk.Entry(self.server_info_frame, show="*")
        self.auth_key_entry.grid(row=3, column=1, sticky="w", pady=2)
        self.connect_button = tk.Button(self.server_info_frame, text="Connect", command=self.connect)
        self.connect_button.grid(row=4, column=0, columnspan=1, pady=5)
        self.connect_indicator = tk.Label(self.server_info_frame, width=1, height=1, bg="gray")
        self.connect_indicator.grid(row=4, column=2)

        # Instance Info
        self.instance_info_frame = tk.Frame(self.master, padx=10, pady=10)
        self.instance_info_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.instance_info_frame, text="Instance Info").grid(row=0, column=0, sticky="w")
        tk.Label(self.instance_info_frame, text="Workspace").grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(self.instance_info_frame, text="Model").grid(row=2, column=0, sticky="w", pady=2)
        tk.Label(self.instance_info_frame, text="Instance").grid(row=3, column=0, sticky="w", pady=2)
        self.workspace_combo = ttk.Combobox(self.instance_info_frame, state="readonly")
        self.workspace_combo.grid(row=1, column=1, sticky="w", pady=2)
        self.model_combo = ttk.Combobox(self.instance_info_frame, state="readonly")
        self.model_combo.grid(row=2, column=1, sticky="w", pady=2)
        self.instance_combo = ttk.Combobox(self.instance_info_frame, state="readonly")
        self.instance_combo.grid(row=3, column=1, sticky="w", pady=2)
        self.workspace_combo.bind("<<ComboboxSelected>>", self.workspace_changed)
        self.model_combo.bind("<<ComboboxSelected>>", self.model_changed)
        self.instance_combo.bind("<<ComboboxSelected>>", self.instance_changed)

        # Instance Tree
        self.instance_tree_frame = tk.Frame(self.master, padx=10, pady=10)
        self.instance_tree_frame.grid(row=1, column=0, sticky="nsew")
        tk.Label(self.instance_tree_frame, text="Instance Tree").pack()
        self.instance_tree = ttk.Treeview(self.instance_tree_frame)
        self.instance_tree.pack(fill="both", expand=True)
    
        # Data
        self.data_frame = tk.Frame(self.master, padx=10, pady=10)
        self.data_frame.grid(row=1, column=1, sticky="nsew")
        tk.Label(self.data_frame, text="Data").pack()
        self.data_text = tk.Text(self.data_frame)
        self.data_text.pack(fill="both", expand=True)
    
        # Menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Documentation", command=self.documentation)
        self.help_menu.add_command(label="About", command=self.about)
    
        # Initialize data
        self.server_ip_entry.insert(0, "18.205.77.131")
        self.server_port_entry.insert(0, "8111")
        self.auth_key_entry.insert(0, "amRlaGFydDpqa2QyMjE0")
        self.workspace_combo["values"] = ["Connect to TWC API..."]
        self.workspace_combo.current(0)
        self.model_combo["values"] = [""]
        self.model_combo.current(0)
        self.instance_combo["values"] = [""]
        self.instance_combo.current(0)

        # Bind the tree view to show the object data
        self.instance_tree.bind('<<TreeviewSelect>>', self.on_treeview_select)
    
    def connect(self):
        server_ip = self.server_ip_entry.get()
        server_port = self.server_port_entry.get()
        auth_key = self.auth_key_entry.get()
    
        call_string = '/osmc/workspaces?includeBody=True'
        url = f'https://{server_ip}:{server_port}{call_string}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {auth_key}"}
        resp_ws = requests.get(url, headers=headers, verify=False)
    
        if resp_ws.status_code == 200:
            self.connect_indicator.config(bg="green")
        else:
            self.connect_indicator.config(bg="red")
    
        workspaces = resp_ws.json()
        self.workspace_ids = {}
        self.workspace_names = {}
    
        for i in range(len(workspaces["ldp:contains"])):
            self.workspace_ids[i] = workspaces["ldp:contains"][i][0]['@id']
            self.workspace_names[i] = workspaces["ldp:contains"][i][1]["dcterms:title"]
    
        self.workspaces_dict = {value: key for key, value in self.workspace_names.items()}
        self.workspace_combo["values"] = list(self.workspace_names.values())
        self.workspace_combo.current(0)
    
    def workspace_changed(self, event):
        
        workspace_name = self.workspace_combo.get()
        workspace_id = self.workspaces_dict[workspace_name]
        workspace_uuid = self.workspace_ids[workspace_id]
    
        call_string = f'/osmc/workspaces/{workspace_uuid}/resources'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call_string}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key_entry.get()}"}
        resp_projects = requests.get(url, headers=headers, verify=False)
        projects_list = resp_projects.json()
        projects_uid_list = projects_list[1]['kerml:resources'] # json list is returned
        
        #self.data_text.delete("1.0", "end")
        #self.data_text.insert("end", len(projects_uid_list))
    
        projects_data = {}
        for i in range(len(projects_uid_list)):
            resource_id = projects_uid_list[i]['@id']
            call = f'/osmc/workspaces/{workspace_uuid}/resources/{resource_id}'
            url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
            resp_projects = requests.get(url, headers=headers, verify=False)
            projects_data[i] = resp_projects.json()
            
        self.project_ids = {}
        self.project_names = {}

        for i in range(len(projects_data)):
             self.project_ids[i] = projects_data[i]['@base'].split("/")[7]
             self.project_names[i] = projects_data[i]['metadata']['name'].split(".")[0]
             
        #self.data_text.delete("1.0", "end")
        #self.data_text.insert("end", self.project_names)
    
        self.model_dict = {value: key for key, value in self.project_names.items()}
        self.model_combo["values"] = list(self.project_names.values())
        self.model_combo.current(0)
        
    def model_changed(self, event):
        
        # need to rename model to project
        model_name = self.model_combo.get()
        model_id = self.model_dict[model_name]
        model_uuid = self.project_ids[model_id]
                                        
        workspace_name = self.workspace_combo.get()
        workspace_id = self.workspaces_dict[workspace_name]
        workspace_uuid = self.workspace_ids[workspace_id]
        
        # So now the funny stuff.. move to a method - all from jupyter demos
        call = f'/osmc/workspaces/{workspace_uuid}/resources/{model_uuid}/revisions'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key_entry.get()}"}
        resp_revList = requests.get(url, headers=headers, verify=False) # turn of verification here since our server is not super secure
        revisionList = resp_revList.json()
        latestRevision = max(revisionList)
        latestRevision
        
        # Then were get the full element list
        sourceRevision = 1
        targetRevision = latestRevision
        call = f'/osmc/workspaces/{workspace_uuid}/resources/{model_uuid}/revisiondiff?source={sourceRevision}&target={targetRevision}'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key_entry.get()}"}
        resp_elementList = requests.get(url,headers=headers, verify=False) # turn of verification here since our server is not super secure
        elementList_json = resp_elementList.json()['added'] # just get the added (availibe items are removed, added, changed, and empty)
        elementList = json.dumps(elementList_json) # push to flat string
        elementList = elementList.replace('"','').replace("[","").replace("]","").replace(" ","") # remove the sting junk
        
        # Now we loop through all of the elements and pull the details (again... needs to be cleaned method)
        call = f'/osmc/resources/{model_uuid}/elements'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
        headers={"accept":"application/ld+json", "Content-Type":"text/plain", "authorization":f"Basic {self.auth_key_entry.get()}"}
        resp_elementListData = requests.post(url,headers=headers, verify=False, data = elementList) # turn of verification here since our server is not super secure
        self.elementListData = resp_elementListData.json() # just get the added (availibe items are removed, added, changed, and empty)
        
        # Load the JSON object into a Python dictionary -- hack for now...
        #with open('./examples/elements.json', 'r') as f:
        #    self.data = json.load(f)
        #    print(type(self.data))

        # OK so now its working locally... just dump into a json file from above
        self.data = self.elementListData

        # Lets loop throug the selected projects elemetns and find the index of all instances
        instanceSpecificationIndex = {}
        for i in range(len(elementList_json)): # Where i is the uuid of the element in this case
            if self.elementListData[elementList_json[i]]['data'][0]['@type'] == ['ldp:DirectContainer', 'uml:InstanceSpecification']:
                instanceSpecificationIndex[i] = i # Add any key to the index that is an istance
                
        # lets create a combobox to list the avalible instances (models) in this workspace
        # Build arrays of the items
        self.instanceIds = {} #indexes not uuids
        self.instanceNames = {}
        
        # Lets build a list of workspaces for selection
        for keys in instanceSpecificationIndex:
            if(self.elementListData[elementList_json[keys]]['data'][1]['kerml:name'])!="": 
                self.instanceIds[keys] = self.elementListData[elementList_json[keys]]
                self.instanceNames[keys] = self.elementListData[elementList_json[keys]]['data'][1]['kerml:name']
        
        #self.data_text.delete("1.0", "end")
        #self.data_text.insert("end", instanceNames)

        self.instance_dict = {value: key for key, value in self.instanceNames.items()}
        self.instance_combo["values"] = list(self.instanceNames.values())
        self.instance_combo.current(0)

        """ write self.data to a file for testing"""
        with open('./examples/elements_latest.json', 'w') as f:
            json.dump(self.data, f, indent=4)

        
    def instance_changed(self, event):
        # clean out any current view
        self.clear_tree()

        # Lets get the instance uuid
        instance_name = self.instance_combo.get()
        instance_id = self.instance_dict[instance_name]
        instance_blob = self.instanceIds[instance_id]
        instance_uuid = instance_blob['data'][0]['ldp:membershipResource']['@id'].replace('#','')
        
        # Lets dump the uuid to the text box
        self.data_text.delete("1.0", "end")
        self.data_text.insert("end", instance_uuid)

        # Lets create the node tree
        # {'data': [{'ldp:membershipResource': {'@id': '#7d73925a-f5af-4d8f-8b04-0a3985b21409'}
        # root_node_id = '7d73925a-f5af-4d8f-8b04-0a3985b21409'  # Replace with the desired root node ID
        root_node_id = instance_uuid    # Replace with the desired root node ID
        root_node = self.create_tree(root_node_id)  # Create the root node
        self.insert_treeview_nodes(self.instance_tree, '', root_node)   # Insert the root node into the treeview

    def clear_tree(self):
        # delete all items in the tree
        for item in self.instance_tree.get_children():
            self.instance_tree.delete(item)
    
    def create_tree(self, node_id):
        node_data = self.data[node_id]['data']  # Get the data of the node
        node_type = node_data[0]['@type'][1]    # Get the type of the node
        node_name = node_id                     # Set the name of the node to the id of the node

        node = Node(node_name) # Create a node object

        # Get the name of the node
        owned_elements = self.data[node_id]['data'][1]['kerml:ownedElement'] # Get the owned elements of the node
        for owned_element in owned_elements:
            element_id = owned_element['@id']   # Get the id of the owned element
            child_node = self.create_tree(element_id)   # Create a node for the owned element
            child_node.parent = node    # Set the parent of the owned element to the current node

        # Get the instance of the node
        try:
            instance = self.data[node_id]['data'][1]['kerml:esiData']['instance'] # Get the instance of the node
            instance_id = instance['@id']   # Get the id of the instance
            child_node = self.create_tree(instance_id)  # Create a node for the instance
            child_node.parent = node    # Set the parent of the instance to the current node
        except KeyError:
            pass
    
        return node # Return the node
    
    # The function to insert nodes into the Treeview
    def insert_treeview_nodes(self, treeview, parent, tree_node):
        treeview_node = treeview.insert(parent, 'end', text=tree_node.name) # Insert the node into the treeview

        # Insert the children of the node into the treeview    
        for child in tree_node.children:
            self.insert_treeview_nodes(treeview, treeview_node, child)

        # Set the node to the open state
        treeview.item(treeview_node, open=True)

    def on_treeview_select(self, event):
        item_id = self.instance_tree.item(self.instance_tree.focus())['text']   # Get the id of the selected item
        if item_id in self.data:    # Check if the id is in the data
            json_data = self.data[item_id]  
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, json.dumps(json_data, indent=2))
        else:
            self.data_text.delete(1.0, tk.END)  # Clear the text box

    def save(self):
        data = {
            "Server IP": self.server_ip_entry.get(),
            "Server Port": self.server_port_entry.get(),
            "Auth Key": self.auth_key_entry.get(),
            "Workspace": self.workspace_combo.get(),
            "Model": self.model_combo.get(),
            "Instance": self.instance_combo.get(),
        }
    
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as f:
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
    
    def load(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "r") as f:
                data = {}
                for line in f:
                    key, value = line.strip().split(": ")
                    data[key] = value
    
                self.server_ip_entry.delete(0, "end")
                self.server_ip_entry.insert(0, data["Server IP"])
                self.server_port_entry.delete(0, "end")
                self.server_port_entry.insert(0, data["Server Port"])
                self.auth_key_entry.delete(0, "end")
                self.auth_key_entry.insert(0, data["Auth Key"])
                self.workspace_combo.set(data["Workspace"])
                self.model_combo.set(data["Model"])
                self.instance_combo.set(data["Instance"])
    
    def documentation(self):
        file_path = os.path.join(os.path.dirname(__file__), "docs.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.data_text.delete("1.0", "end")
                self.data_text.insert("end", f.read())
        else:
            tk.messagebox.showerror("Error", "Documentation file not found.")
    
    def about(self):
        tk.messagebox.showinfo("About", "My App v1.0")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    
