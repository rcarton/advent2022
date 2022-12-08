import io

from advent.days.day05 import first, parse, second

data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
data_io = io.StringIO(data)


def test_first():
    assert first(io.StringIO(data)) == 'CMZ'


def test_second():
    assert second(io.StringIO(data)) == 'MCD'
