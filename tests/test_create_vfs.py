from wgrd_cons_tools.create_vfs import *

def test_search_vfs_tree():
    test_tree = {"a\\b": "test1.dat", "a\\c": "test2.dat", "a\\b\\c": "test3.dat"}
    assert(search_vfs_tree(test_tree, "a/b") == {"a\\b": "test1.dat", "a\\b\\c": "test3.dat"})
    assert(search_vfs_tree(test_tree, "a\\c") == {"a\\c": "test2.dat"})

