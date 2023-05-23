import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.treeview = ttk.Treeview(root)
        self.treeview.pack(fill=tk.BOTH, expand=1)

        self.treeview.bind('<Button-3>', self.show_context_menu)

        self.context_menus = {
            'main': self.create_main_context_menu(),
            'root': self.create_root_context_menu(),
            'branch': self.create_branch_context_menu()
        }

    def show_context_menu(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        if not item:
            self.context_menus['main'].tk_popup(event.x_root, event.y_root)
        else:
            tags = self.treeview.item(item, "tags")
            if 'root' in tags:
                self.context_menus['root'].tk_popup(event.x_root, event.y_root)
            elif 'branch' in tags:
                self.context_menus['branch'].tk_popup(event.x_root, event.y_root)

    def create_main_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Create Project', command=self.create_project)
        return menu

    def create_root_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Add Branch', command=self.add_branch)
        return menu

    def create_branch_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Add Leaf', command=self.add_leaf)
        return menu

    def create_project(self):
        project_name = 'Project'
        self.treeview.insert('', tk.END, text=project_name, tags=('root',))

    def add_branch(self):
        selected_item = self.treeview.selection()[0]
        branch_name = 'Branch'
        self.treeview.insert(selected_item, tk.END, text=branch_name, tags=('branch',))

    def add_leaf(self):
        selected_item = self.treeview.selection()[0]
        leaf_name = 'Leaf'
        self.treeview.insert(selected_item, tk.END, text=leaf_name)

def main():
    root = tk.Tk()
    root.geometry('300x400')
    root.title('Treeview GUI')
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
