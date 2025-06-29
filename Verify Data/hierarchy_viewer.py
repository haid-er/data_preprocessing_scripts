import os
from anytree import Node, RenderTree
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def build_hierarchy(path):
    """Build a hierarchical tree structure from a directory path."""
    def add_nodes(current_path, parent_node):
        for entry in sorted(os.listdir(current_path)):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                node = Node(entry, parent=parent_node, file_count=0)
                add_nodes(entry_path, node)
            else:
                parent_node.file_count += 1

    root_name = os.path.basename(path.rstrip(os.sep)) or path
    root = Node(root_name, file_count=0)
    add_nodes(path, root)
    return root

def display_hierarchy_with_file_count(root):
    """Display the hierarchy tree and file counts at all levels with colors."""
    def count_files(node):
        if not node.children:
            return node.file_count
        total = 0
        for child in node.children:
            total += count_files(child)
        node.file_count = total
        return total

    count_files(root)  # Populate file counts for all nodes

    for pre, _, node in RenderTree(root):
        file_info = f" [Files: {node.file_count}]" if node.file_count > 0 else ""

        if node.is_root:
            color = Fore.GREEN  # Device name
        elif node.parent.is_root:
            color = Fore.BLUE  # Subject name
        elif node.parent.parent.is_root:
            color = Fore.CYAN
        else:
            color = Fore.YELLOW  # Activity name

        print(f"{pre}{color}{node.name}{file_info}{Style.RESET_ALL}")

def main():
    print("Welcome to the Hierarchy Viewer!")
    path = input("Enter the directory path: ").strip()

    if not os.path.exists(path):
        print("Invalid path. Please try again.")
        return

    root = build_hierarchy(path)
    print("\nHierarchy:")
    display_hierarchy_with_file_count(root)
    
if __name__ == "__main__":
    main()
