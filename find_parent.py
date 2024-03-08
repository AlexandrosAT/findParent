import os


class File:
    def __init__(self, name) -> None:
        self.children = []
        self.name = name

    def add_child(self, file) -> None:
        self.children.append(file)

    def print_tree(self, indent="") -> None:
        print(f"{indent}+ {self.name}")
        for child in self.children:
            child.print_tree(indent + "|   ")


def process_current_node(nodes_to_search: list, current_path_stack: list) -> None:
    """
    DFS logic to traverse children
    Parameters:
    - nodes_to_search (list): List with the nodes to be processed.
    - current_path_stack (list): List of the current file path.
    """
    # Expand the children of a parent folder, append them to the nodes and remove the parent
    # In case we already have the folder in the stack, we don't expand to avoid circular dependencies
    # See README.md for further explanation
    if (
        nodes_to_search[-1][0].children
        and nodes_to_search[-1][0].name not in current_path_stack
    ):
        nodes_to_search.append(nodes_to_search[-1][0].children.copy())
        current_path_stack.append(nodes_to_search[-2][0].name)
        del nodes_to_search[-2][0]

    # Remove sublist if no more children are remaining
    else:
        if len(nodes_to_search[-1]) > 1:
            del nodes_to_search[-1][0]
        else:
            del nodes_to_search[-1]
            current_path_stack.pop()
            # We have traversed the depth of the tree
            while nodes_to_search and len(nodes_to_search[-1]) == 0:
                del nodes_to_search[-1]
                current_path_stack.pop()


def build_common_path(file_path_stack1: list, file_path_stack2: list) -> str:
    """
    Compares two file paths and returns the common path between them.

    Parameters:
    - file_path_stack1 (list): List of the file path for the first file.
    - file_path_stack2 (list): List of the file path for the second file.

    Returns:
    str: The common path.
    """
    i = 0
    common_path = []
    while (
        i < min(len(file_path_stack1), len(file_path_stack2))
        and file_path_stack1[i] == file_path_stack2[i]
    ):
        common_path.append(file_path_stack2[i])
        i += 1

    return common_path


def build_longest_common_path(file_path_stack: dict) -> list:
    """
    Generates all possible common paths for the two files and returns the longest one.

    Parameters:
    - file_path_stack (dict): All the paths of the two files.

    Returns:
    str: The first parent folder that contains both files.
    """
    keys = list(file_path_stack.keys())
    if len(keys) != 2:
        raise ValueError("Dictionary should have paths for two files")

    paths = []
    for first_file in file_path_stack[keys[0]]:
        for second_file in file_path_stack[keys[1]]:
            paths.append(build_common_path(first_file, second_file))
    longest_path = max(paths, key=len)

    return os.path.join(*longest_path)


def find_parent(root: File, first_file: str, second_file: str) -> str:
    """
    Finds the common path of two files in a file system.

    Parameters:
    - root (File): The root of the file system.
    - first_file (str): Name of the first file in question.
    - second_file (str): Name of the second file in question.

    Returns:
    str: The first parent folder that contains both files.
    """

    if root == None:
        raise ValueError("File system not provided. Please provide a valid root.")

    if len(root.children) == 0:
        raise FileNotFoundError("File system is empty")

    # Stack keeping track of the current path during traversal
    current_path_stack = [root.name]
    # Stores the paths for the two files
    files_path_stacks = {}
    search_terms = [first_file, second_file]
    # Maintaines the current set of nodes to be explored
    nodes_to_search = [root.children.copy()]

    # Traversal of the file tree with DFS
    while nodes_to_search:
        # Storing path if file is found
        if nodes_to_search[-1][0].name in search_terms:
            files_path_stacks[nodes_to_search[-1][0].name] = [current_path_stack.copy()]

        process_current_node(nodes_to_search, current_path_stack)

    if len(files_path_stacks) != 2 and not nodes_to_search:
        raise FileNotFoundError(
            f"Files not found: {', '.join(file_name for file_name in search_terms)}"
        )

    return build_longest_common_path(files_path_stacks)
