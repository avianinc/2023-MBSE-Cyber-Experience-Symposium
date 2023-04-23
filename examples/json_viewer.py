import tkinter as tk
import json

class TreeViewApp:
    def __init__(self, master):
        self.master = master
        self.tree = tk.ttk.Treeview(master)
        self.tree.pack(fill=tk.BOTH, expand=True)

        with open('./examples/elements_latest.json', 'r') as f:
            data = json.load(f)

        self._populate_tree(data, "")

    def _populate_tree(self, node, parent):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict) or isinstance(value, list):
                    item_id = self.tree.insert(parent, 'end', text=key)
                    self._populate_tree(value, item_id)
                else:
                    self.tree.insert(parent, 'end', text=key, values=(value,))
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, dict) or isinstance(item, list):
                    item_id = self.tree.insert(parent, 'end', text="")
                    self._populate_tree(item, item_id)
                else:
                    self.tree.insert(parent, 'end', text="", values=(item,))

if __name__ == '__main__':
    root = tk.Tk()
    app = TreeViewApp(root)
    root.mainloop()
