#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 10:00
# @Author  : John_DeHart
# @Site    : AVIAN Inc.
# @Software: NA
# @Code    : TWC API Interactions - Demo
# @Desc    : Base GUI for TWC API Interactions to support MBSECCES
"""
TWC and Intsance interfacing demonstration: This tool demonstartes 
communicationswith Cameos Teamwork Cloud API and interrogating an 
instance. The instance can be reviewed and written to disk according 
to the needs of the simulation toolset.

Author: J.K. DeHart
Date: 3/2/2023
Comapny: AVIAN Inc.
"""
# Import the required libraries
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import filedialog
from anytree import Node
import os
import requests
import json
from tkinter import filedialog
import re

class CustomNode(Node):
    # Created to add some additional attributes to the node
    def __init__(self, name, nodeName = None, uuid=None, type=None, documentation=None, value=None, parent=None):
        super().__init__(name, parent=parent)
        self.uuid = uuid
        self.type = type
        self.value = value
        self.nodeName = nodeName
        self.documentation = documentation

class App:
    # Main application class
    def __init__(self, master):
        self.master = master
        self.master.title("TWC API Interactions - Demo")
        self.master.geometry("960x680")

        # Configure the column weights to allow the paned window to expand
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        # Left Frames Container
        self.left_frames_container = tk.Frame(self.master)
        self.left_frames_container.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Server Info Frame
        self.server_info_frame = tk.Frame(self.master, padx=10, pady=10)
        self.server_info_frame.grid(row=0, column=0, sticky="nw")

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

        # Instance Info Frame
        self.instance_info_frame = tk.Frame(self.master, padx=10, pady=10)
        self.instance_info_frame.grid(row=1, column=0, sticky="nw")

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
        
        # Separator between server info and instance tree/text area
        self.separator = ttk.Separator(self.master, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Create a paned window to add the separator
        self.paned_window = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # Instance Tree
        self.instance_tree_frame = tk.Frame(self.paned_window, padx=10, pady=10)
        tk.Label(self.instance_tree_frame, text="Instance Tree").pack()
        self.instance_tree = ttk.Treeview(self.instance_tree_frame)
        self.instance_tree.pack(side="left", fill="both", expand=True)

        # Add scrollbar to tree view
        self.tree_scrollbar = ttk.Scrollbar(self.instance_tree_frame, orient="vertical", command=self.instance_tree.yview)
        self.tree_scrollbar.pack(side="right", fill="y")
        self.instance_tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # Add instance_tree_frame to paned window
        self.paned_window.add(self.instance_tree_frame)

        # Data
        self.data_frame = tk.Frame(self.paned_window, padx=10, pady=10)
        tk.Label(self.data_frame, text="Data").pack()

        # Add scrollbar to text area
        self.text_scrollbar = ttk.Scrollbar(self.data_frame, orient="vertical")
        self.text_scrollbar.pack(side="right", fill="y")

        # Add text area
        self.data_text = tk.Text(self.data_frame, yscrollcommand=self.text_scrollbar.set)
        self.data_text.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        self.text_scrollbar.config(command=self.data_text.yview)

        # Add data_frame to paned window
        self.paned_window.add(self.data_frame)

        # Bind the tree view to show the object data and open a new window on double click
        self.instance_tree.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.instance_tree.bind('<Double-1>', self.on_treeview_double_click)

        # Menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Server Info", command=self.save)
        self.file_menu.add_command(label="Load Server Info", command=self.load)
        self.export_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Export", menu=self.export_menu)
        self.export_menu.add_command(label="Export Model Elements", command=self.save_data)
        self.export_menu.add_command(label="Export Instance Tree", command=self.export_instance_tree_as_json)
        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Documentation", command=self.documentation)
        self.help_menu.add_command(label="About", command=self.about)
    
        # Initialize data
        self.server_ip_entry.insert(0, "18.205.77.131")
        self.server_port_entry.insert(0, "8111")
        self.auth_key_entry.insert(0, "amRlaGFydDpqa2QyMjE0") # clean this from the code before pushing to github
        self.workspace_combo["values"] = ["Connect to TWC API..."]
        self.workspace_combo.current(0)
        self.model_combo["values"] = [""]
        self.model_combo.current(0)
        self.instance_combo["values"] = [""]
        self.instance_combo.current(0)
        self.data_text.insert(tk.END, "Select an instance to view its data.")
        #self.data_text.config(state=tk.DISABLED)

        # Bind the tree view to show the object data
        self.instance_tree.bind('<<TreeviewSelect>>', self.on_treeview_select)
    
        # Configure the column and row weights
        self.master.columnconfigure(0, weight=0, minsize=300)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)

        # Button Frame
        #self.button_frame = tk.Frame(self.master, padx=10, pady=10)
        #self.button_frame.grid(row=3, column=1, sticky="nsew")

        # Export Button
        #self.export_button = tk.Button(self.button_frame, text="Export Tree as JSON", command=self.export_instance_tree_as_json)
        #self.export_button.pack()

    def on_treeview_double_click(self, event):
        item = self.instance_tree.selection()[0]
        item_text = self.instance_tree.item(item, "text")

        # extract the uuid insde the parentesiese from the item text
        item_text = item_text[item_text.find("(")+1:item_text.find(")")]
        
        new_window = tk.Toplevel(self.master)
        new_window.title("New Window")
        new_window.geometry("300x200")

        label = tk.Label(new_window, text=f"Selected item: {item_text}")
        label.pack(padx=10, pady=10)

        # Assuming 'data' is a dictionary containing your treeview data
        value = self.data[item_text]['data'][1]['kerml:esiData']['value']

        value_label = tk.Label(new_window, text="Value")
        value_label.pack(padx=10, pady=(0, 5))
        
        value_entry = tk.Entry(new_window)
        value_entry.pack(padx=10, pady=(0, 10))
        value_entry.insert(0, value)

        # Add a button that calls the 'update_literal_real_value_thru_api' function
        #update_button = tk.Button(new_window, text="Update Value", command=self.update_literal_real_value_thru_api)
        #update_button.pack(pady=(0, 10))

        # Add a button that calls the 'update_literal_real_value_thru_api' function with the updated value and item_text
        update_button = tk.Button(new_window, text="Update Value",
                                  command=lambda: self.update_literal_real_value_thru_api(value_entry.get(), item_text))
        update_button.pack(pady=(0, 10))

    def update_literal_real_value_thru_api(self, value, uuid):
        # Your implementation to update the value through API
        print(f"Update value through API {value}")

        # Create the payload
        dataValue = {"kerml:esiData":{"value":"0.0"}} # Build the data payload
        dataValue["kerml:esiData"]["value"] = value # Update the json string
        
        # Now build the api call
        call_string = f'/osmc/resources/{self.model_uuid}/elements/{uuid}'
        url = f'https://{self.server_ip}:{self.server_port}{call_string}'
        headers={"accept":"application/ld+json", "authorization":f"Basic {self.auth_key}", "Content-Type":"application/ld+json"}
        
        # Have to add a new header of content type
        resp_value = requests.patch(url, headers = headers, verify = False, json = dataValue) # turn of verification here since our server is not super secure
        print(url)
        print(dataValue)

        # resp_value.status_code
        # print(dataValue)
        print(resp_value.content)

    def connect(self):
        # Get the server info
        self.server_ip = self.server_ip_entry.get()
        self.server_port = self.server_port_entry.get()
        self.auth_key = self.auth_key_entry.get()

        # Get the workspaces 
        call_string = '/osmc/workspaces?includeBody=True'
        url = f'https://{self.server_ip}:{self.server_port}{call_string}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key}"}
        resp_ws = requests.get(url, headers=headers, verify=False)

        # Check the response
        if resp_ws.status_code == 200:
            self.connect_indicator.config(bg="green")
        else:
            self.connect_indicator.config(bg="red")

        # Parse the response
        workspaces = resp_ws.json()
        self.workspace_ids = {}
        self.workspace_names = {}

        # Loop through the workspaces and add them to the combo box
        for i in range(len(workspaces["ldp:contains"])):
            self.workspace_ids[i] = workspaces["ldp:contains"][i][0]['@id']
            self.workspace_names[i] = workspaces["ldp:contains"][i][1]["dcterms:title"]
    
        # Set the combo box values
        self.workspaces_dict = {value: key for key, value in self.workspace_names.items()}
        self.workspace_combo["values"] = list(self.workspace_names.values())
        self.workspace_combo.current(0)
    
    def workspace_changed(self, event):
        # Get the workspace name and id
        workspace_name = self.workspace_combo.get()
        workspace_id = self.workspaces_dict[workspace_name]
        workspace_uuid = self.workspace_ids[workspace_id]
    
        # Get the projects
        call_string = f'/osmc/workspaces/{workspace_uuid}/resources'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call_string}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key_entry.get()}"}
        resp_projects = requests.get(url, headers=headers, verify=False)
        projects_list = resp_projects.json()
        projects_uid_list = projects_list[1]['kerml:resources'] # json list is returned
        
        #self.data_text.delete("1.0", "end")
        #self.data_text.insert("end", len(projects_uid_list))

        # Get the project data
        projects_data = {}

        # Loop through the projects and get the data
        for i in range(len(projects_uid_list)):
            resource_id = projects_uid_list[i]['@id']
            call = f'/osmc/workspaces/{workspace_uuid}/resources/{resource_id}'
            url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
            resp_projects = requests.get(url, headers=headers, verify=False)
            projects_data[i] = resp_projects.json()
            
        # Get the project names and ids
        self.project_ids = {}
        self.project_names = {}

        # Loop through the projects and add them to the combo box
        for i in range(len(projects_data)):
             self.project_ids[i] = projects_data[i]['@base'].split("/")[7]
             self.project_names[i] = projects_data[i]['metadata']['name'].split(".")[0]
             
        #self.data_text.delete("1.0", "end")
        #self.data_text.insert("end", self.project_names)

        # Set the combo box values
        self.model_dict = {value: key for key, value in self.project_names.items()}
        self.model_combo["values"] = list(self.project_names.values())
        self.model_combo.current(0)
        
    def model_changed(self, event):
        # Get the model name and id (project in CSM lingo)
        self.model_name = self.model_combo.get()
        self.model_id = self.model_dict[self.model_name]
        self.model_uuid = self.project_ids[self.model_id]
                                        
        # Get the workspace name and id
        self.workspace_name = self.workspace_combo.get()
        self.workspace_id = self.workspaces_dict[self.workspace_name]
        self.workspace_uuid = self.workspace_ids[self.workspace_id]
        
        # So now the funny stuff.. move to a method - all from jupyter demos
        # First we get the latest revision
        call = f'/osmc/workspaces/{self.workspace_uuid}/resources/{self.model_uuid}/revisions'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key_entry.get()}"}
        resp_revList = requests.get(url, headers=headers, verify=False) # turn of verification here since our server is not super secure
        revisionList = resp_revList.json()
        latestRevision = max(revisionList)
        latestRevision
        
        # Then were get the full element list
        sourceRevision = 1
        targetRevision = latestRevision
        call = f'/osmc/workspaces/{self.workspace_uuid}/resources/{self.model_uuid}/revisiondiff?source={sourceRevision}&target={targetRevision}'
        url = f'https://{self.server_ip_entry.get()}:{self.server_port_entry.get()}{call}'
        headers = {"accept": "application/ld+json", "authorization": f"Basic {self.auth_key_entry.get()}"}
        resp_elementList = requests.get(url,headers=headers, verify=False) # turn of verification here since our server is not super secure
        elementList_json = resp_elementList.json()['added'] # just get the added (availibe items are removed, added, changed, and empty)
        elementList = json.dumps(elementList_json) # push to flat string
        elementList = elementList.replace('"','').replace("[","").replace("]","").replace(" ","") # remove the sting junk
        
        # Now we loop through all of the elements and pull the details (again... needs to be cleaned method)
        call = f'/osmc/resources/{self.model_uuid}/elements'
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

        # Set the combo box values
        self.instance_dict = {value: key for key, value in self.instanceNames.items()}
        self.instance_combo["values"] = list(self.instanceNames.values())
        self.instance_combo.current(0)

        # Lets dump the json to a file for now
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
        # Create a node object
        node_data = self.data[node_id]['data']  # Get the data of the node
        node_type = node_data[0]['@type'][1]    # Get the type of the node
        node_uuid = node_id                     # Set node uuid to the id of the node 

        # Set node name based on type
        if node_type == 'uml:InstanceSpecification':
            node_name = node_data[1]['kerml:name']   # Set the name of the node to the name of the instance
        elif node_type == 'uml:Slot':
            # to name a slot you must find the defining feature and use its name
            slotDefiningFeature = self.data[node_id]['data'][1]['kerml:esiData']['definingFeature']['@id']
            node_name = self.data[slotDefiningFeature]['data'][1]['kerml:name']
        elif node_type == "uml:Comment":
            node_name = "Comment"
        elif node_type == 'uml:InstanceValue':
            node_name = 'Instance'
        elif node_type == 'uml:LiteralReal' or node_type == 'uml:LiteraString' or node_type == 'uml:LiteralBoolean' or node_type == 'uml:LiteralInteger':
            node_name = node_data[1]['kerml:esiData']['value']

        # Create a node object
        # Using a CustomNode class to store the node data
        try:
            #node = CustomNode(name=node_uuid, nodeName=node_name, uuid=node_uuid, type=node_type)  # Create a node object
            node = CustomNode(name=node_name+' ('+node_uuid+')', uuid=node_uuid, type=node_type)  # Create a node object
        except UnboundLocalError:
            node = CustomNode("Unknown", "", "")

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
        # Get the id of the selected item
        item_id = self.instance_tree.item(self.instance_tree.focus())['text']

        # lets extract the uuid from the name (kinda hacky since I cant find the node attributes)
        item_id = item_id.split('(')[1].split(')')[0]

        # Get the data of the selected item
        if item_id in self.data:    # Check if the id is in the data
            json_data = self.data[item_id]  
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, json.dumps(json_data, indent=2))
        else:
            self.data_text.delete(1.0, tk.END)  # Clear the text box

    def save(self):
        # Get the data from the entries
        data = {
            "Server IP": self.server_ip_entry.get(),
            "Server Port": self.server_port_entry.get(),
            "Auth Key": self.auth_key_entry.get(),
            "Workspace": self.workspace_combo.get(),
            "Model": self.model_combo.get(),
            "Instance": self.instance_combo.get(),
        }

        # Save the data to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as f:
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
    
    def load(self):
        # Load the data from a file
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
        # Open the documentation file
        file_path = os.path.join(os.path.dirname(__file__), "docs.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.data_text.delete("1.0", "end")
                self.data_text.insert("end", f.read())
        else:
            tk.messagebox.showerror("Error", "Documentation file not found.")
    
    def about(self):
        # Show the about message
        tk.messagebox.showinfo("About", "My App v1.0")

    def export_instance_tree_as_json(self):
        # Get the filename to save the JSON file as
        filename = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON Files', '*.json')])
        if not filename:
            return
        
        # Get the data and attributes to build a json file from the instance tree
        #tree_data = self.get_tree_data(self.instance_tree, self.instance_tree.get_children()[0])
        tree_data = self.get_tree_data(self.instance_tree, "")

        # Process the data to remove the instance and name keys
        processed_data_A = self.process_dict(tree_data)
        processed_data_B = self.separate_uuids(processed_data_A)

        # Save the data to a JSON file
        with open(filename, "w") as json_file:
            json.dump(processed_data_B, json_file, ensure_ascii=True, indent=2)

    def process_dict(self, d):
        # this function cleans the json data from the treeview removing the instance and name keys
        new_dict = {}
        for k, v in d.items():
            if k.lower().startswith('instance') or k.lower().startswith('name') or k.lower().startswith('attributes'):
                if isinstance(v, dict):
                    new_dict.update(self.process_dict(v))
            else:
                if isinstance(v, dict):
                    new_dict[k] = self.process_dict(v)
                else:
                    new_dict[k] = v
        return new_dict

    def separate_uuids(self, obj, parent_key=None):
        # This function separates the uuid from the name in the treeview and adds it to the attributes
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                match = re.match(r'^(.*?) \((.*?)\)$', key)
                if match:
                    new_key, uuid = match.groups()
                    new_value = self.separate_uuids(value, new_key)
                    item = {"name": new_key, "uuid": uuid, "attributes": new_value}
                else:
                    new_key = key
                    new_value = self.separate_uuids(value, parent_key)
                    item = {"name": new_key, "attributes": new_value}
                new_obj[new_key] = item
            return new_obj
        elif isinstance(obj, list):
            return [self.separate_uuids(item, parent_key) for item in obj]
        else:
            return obj    

    def save_data(self):
        # Get the filename to save the JSON file as
        filename = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON Files', '*.json')])
        if not filename:
            return
        
        # Get the data from the instance tree
        elements_data = self.data

        # Save the data to a JSON file
        with open(filename, "w") as json_file:
            json.dump(elements_data, json_file, ensure_ascii=True, indent=4)

    def get_tree_data(self, tree, node):
        # Get the data from the tree
        children = tree.get_children(node)

        # Check if the node has children
        if not children:
            item_data = tree.item(node)
            node_data = {
                "name": item_data["text"],
                "attributes": item_data["values"][1:],  # Use slicing to exclude the "Icon" value
            }
            # Add the data from the data dictionary
            if item_data["text"] in self.data:
                node_data.update(self.data[item_data["text"]])
            return node_data
        
        # Get the data from the children
        node_data = {}

        # Loop through the children
        for child in children:
            child_data = self.get_tree_data(tree, child)
            if child_data:
                node_data[tree.item(child, "text")] = child_data
        return node_data

if __name__ == "__main__":
    # Create the root window
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    
