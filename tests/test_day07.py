import io

from advent.days.day07 import first, parse, second

data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
data_io = io.StringIO(data)


def test_parse():
    assert parse(data).get_size() == 48381165


def test_first():
    assert first(io.StringIO(data)) == 95437


def test_second():
    assert second(io.StringIO(data)) == 24933642
