# File System Parent Finder

## Description

This Python module provides a solution for finding the common parent folder of two files in a file system. The implementation includes a `File` class representing the file system structure and a function `find_parent` to determine the common parent.

## Table of contents

1. [Usage](#usage)
   1. [File Class](#file-class)
   2. [find_parent Function](#find_parent-function)
   3. [Testing](#testing)
2. [Analysis](#analysis)
3. [Considerations](#considerations)

## Usage

### File Class

The `File` class is used to represent the structure of the file system. It has the following methods:

- `__init__(self, name)`: Initializes a new instance of the `File` class with the specified name.
- `add_child(self, file)`: Adds a child file to the current file.
- `print_tree(self, indent="")`: Prints a tree structure of the file system.

### find_parent Function

The `find_parent` function takes three parameters:

- `root`: The root of the file system (an instance of the `File` class).
- `first_file`: The name of the first file.
- `second_file`: The name of the second file.

The function returns the first parent folder that contains both files.

```python
# Example Usage

# Creating a file system structure
root = File("root")
a = File("a")
b = File("b")
c = File("c")
d = File("d")

root.add_child(a)
root.add_child(b)
a.add_child(c)
a.add_child(d)

# Printing the file system structure
root.print_tree()

# Finding the common parent of two files
common_parent = find_parent(root, "c", "d")
print(f"The common parent is: {common_parent}")
```

### Testing

Feel free to explore the provided unit tests to understand various scenarios and how the solution behaves in different situations. The unit tests cover cases such as empty file systems, circular dependencies, simple file systems, and large file systems with common parent scenarios.

You can run the tests by executing
`python3 test_module.py`

## Analysis

The solution employs a depth-first search (DFS) approach to traverse the file system. The `process_current_node` function handles the DFS logic, and the `build_common_path` and `build_longest_common_path` functions are responsible for comparing file paths and determining the common parent.

Circular dependencies are avoided during traversal to prevent infinite loops. If a parent folder is encountered again in the traversal stack, it is not expanded to avoid circular dependencies.

The iterative approach to the algorithm has been chosen for two reasons:

1. With the expected size of a real file system, a recursive approach would hinder performance.
2. A recursive approach searching for both file names could make the code more complex and harder to read.

## Considerations

- **File Class** For this solution, the class `File` has been used as is from the Boilerplate. Though useful for a simple solution, more data should be used in order to avoid the following tradeoffs:

  - _Distinct names_: The solution has been developed with the assumption that all folders and files have distinct names. without this assumption and an expanded 'File' class, the solution would not be foolproof (same as comparing two folders with `diff -r folder1 folder2`) while having reduced performance. Adding data like inode to the structure and replacing the usage of name with it would provide distinctness for the files and folders.

- **Memory Usage:** The implementation uses a depth-first search (DFS) approach with a stack for traversal. While this avoids recursion, it still maintains a stack to keep track of the current nodes to be explored. For deep file systems, the stack may contribute to higher memory usage.

- **Performance:** The current implementation uses a while loop for DFS, which is generally efficient. However, for extremely large file systems, further optimizations might be explored for better performance.

- **Algorithm Complexity:** The algorithm complexity is generally linear with respect to the number of nodes in the file system. However, for extremely large file systems, the linear search for the common parent might become a performance bottleneck. Advanced algorithms or data structures, such as indexing or caching, could be considered for optimization.
