from anytree import Node, RenderTree

class CustomNode(Node):
    def __init__(self, name, color=None, parent=None):
        super().__init__(name, parent=parent)
        self.color = color

# Create the nodes with the custom class
root = CustomNode("Root")
item_A = CustomNode("item_A", color="Red", parent=root)
item_B = CustomNode("item_B", color="Blue", parent=root)

# Access the color attribute
print(item_A.color)  # Output: Red

# Print the tree
for pre, _, node in RenderTree(root):
    print(f"{pre}{node.name}({node.color})")

# Output:
# Root
# ├── item_A
# └── item_B
