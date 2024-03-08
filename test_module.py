import unittest
import json
from find_parent import File, find_parent


def create_structure(node_name: str, structure: list) -> File:
    node = File(node_name)
    for name in structure[node_name]:
        child = create_structure(name, structure)
        node.add_child(child)
    return node


class TestParent(unittest.TestCase):
    def test_empty_file_system(self):
        root = create_structure("root", {"root": []})
        with self.assertRaises(FileNotFoundError):
            find_parent(root, "file1", "file2")

    def test_single_node(self):
        root = create_structure("root", {"root": ["a", "b"], "a": [], "b": []})
        self.assertEqual(find_parent(root, "a", "b"), "root")

    def test_circular_dependencies(self):
        root = File("root")
        folder1 = File("folder1")
        folder2 = File("folder2")
        root.add_child(folder1)
        folder1.add_child(folder2)
        folder2.add_child(root)
        self.assertEqual(find_parent(root, "folder1", "folder2"), "root")

    def test_simple_file_system(self):
        root = create_structure(
            "root", {"root": ["a", "b"], "a": ["c", "d"], "c": [], "d": [], "b": []}
        )
        self.assertEqual(find_parent(root, "c", "d"), "root/a")

    def test_single_child_tree(self):
        root = create_structure(
            "root",
            {"root": ["a"], "a": ["b"], "b": ["c"], "c": ["d"], "d": []},
        )
        self.assertEqual(find_parent(root, "c", "d"), "root/a/b")

    def test_case_sensitivity(self):
        root = create_structure(
            "root", {"root": ["a", "b"], "a": ["c", "d"], "c": [], "d": [], "b": []}
        )
        with self.assertRaises(FileNotFoundError):
            find_parent(root, "A", "b")

    def test_large_file_system(self):
        with open("large_file_system_test_data.json", "r") as file:
            large_file_system_data = json.load(file)
        root = create_structure("root", large_file_system_data)
        self.assertEqual(find_parent(root, "ae", "v"), "root/e/n/u")

    # Adding folder u as a child of k, both root/c/k/u and root/e/n/u paths could be accepted
    def test_large_file_system_common_parent1(self):
        with open("large_file_system_test_data.json", "r") as file:
            large_file_system_data = json.load(file)
            large_file_system_data["k"] = ["u"]
        root = create_structure("root", large_file_system_data)

        self.assertEqual(find_parent(root, "ae", "v"), "root/e/n/u" or "root/c/k/u")

    # Adding folder w as a child of k
    # In this case we could have either root or "root/e/n/u" as parent folder
    # "root/e/n/u" is accepted since it's the first that both ae and v have as a common parent
    def test_large_file_system_common_parent2(self):
        with open("large_file_system_test_data.json", "r") as file:
            large_file_system_data = json.load(file)
            large_file_system_data["k"] = ["w"]
        root = create_structure("root", large_file_system_data)
        self.assertEqual(find_parent(root, "ae", "v"), "root/e/n/u")


if __name__ == "__main__":
    unittest.main()
