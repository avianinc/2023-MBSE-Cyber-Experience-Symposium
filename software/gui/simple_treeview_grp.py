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
            'branch': self.create_branch_context_menu(),
            'group': self.create_group_context_menu()
        }

    def show_context_menu(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        if not item:
            self.context_menus['main'].post(event.x_root, event.y_root)
        else:
            tags = self.treeview.item(item, "tags")
            if 'root' in tags:
                self.treeview.selection_set(item)
                self.context_menus['root'].post(event.x_root, event.y_root)
            elif 'branch' in tags:
                self.treeview.selection_set(item)
                self.context_menus['branch'].post(event.x_root, event.y_root)
            elif 'group' in tags:
                self.treeview.selection_set(item)
                self.context_menus['group'].post(event.x_root, event.y_root)


    def create_main_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Create Mission', command=self.create_project)
        return menu

    def create_root_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Add Performer', command=self.add_branch)
        menu.add_command(label='Add Group', command=self.add_group)
        menu.add_command(label='Rename', command=self.rename_node)
        return menu

    def create_branch_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Add Component', command=self.add_leaf)
        menu.add_command(label='Add Copy to Group', command=self.add_copy_to_group)
        menu.add_command(label='Rename', command=self.rename_node)
        return menu

    def create_group_context_menu(self):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(label='Add Performer', command=self.add_branch_to_group)
        menu.add_command(label='Rename', command=self.rename_node)
        return menu

    def create_project(self):
        project_name = 'Mission Model'
        self.treeview.insert('', tk.END, text=project_name, tags=('root',))

    def add_branch(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        branch_name = 'Performer'
        self.treeview.insert(selected_item, tk.END, text=branch_name, tags=('branch',))

    def add_group(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        group_name = 'Group'
        self.treeview.insert(selected_item, tk.END, text=group_name, tags=('group',))

    def add_leaf(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        leaf_name = 'Component'
        self.treeview.insert(selected_item, tk.END, text=leaf_name)

    def add_copy_to_group(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        selected_item_text = self.treeview.item(selected_item, 'text')
        group_item = None

        for project_child in self.treeview.get_children():
            if self.treeview.item(project_child, "tags")[0] == 'root':
                for child in self.treeview.get_children(project_child):
                    if self.treeview.item(child, "tags")[0] == 'group':
                        group_item = child
                        break

        if group_item:
            self.treeview.insert(group_item, tk.END, text=selected_item_text, tags=('branch',))


    def add_branch_to_group(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        branch_name = 'Branch'
        self.treeview.insert(selected_item, tk.END, text=branch_name, tags=('branch',))

    def rename_node(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]

        entry = ttk.Entry(self.treeview, width=20)
        entry.place(x=self.treeview.bbox(selected_item)[0], y=self.treeview.bbox(selected_item)[1])

        def save_changes(event=None):
            new_text = entry.get()
            if new_text:
                self.treeview.item(selected_item, text=new_text)
            entry.destroy()

        entry.bind('<Return>', save_changes)
        entry.bind('<FocusOut>', save_changes)
        entry.focus_set()

def main():
    root = tk.Tk()
    root.geometry('300x400')
    root.title('Treeview GUI')
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
