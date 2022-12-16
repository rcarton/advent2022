import io

from advent.days.day15 import Sensor, dist, first, parse, row_intersect, second

data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
data_io = io.StringIO(data)


def test_intersect():
    sensors = parse(data)

    for s in sensors:
        print(s.pos[::-1])
        for row in range(0, 21):
            m = ['.'] * 21
            inter = row_intersect(row, s)
            if inter:
                for c in range(max(0, inter[0]), min(21, inter[1] + 1)):
                    m[c] = '#'

            sr, sc = s.pos
            br, bc = s.beacon
            if sr == row and 0 <= sc <= 20:
                m[sc] = 'S'
            if br == row and 0 <= bc <= 20:
                m[bc] = 'B'
            print(''.join(m))

def test_dist():
    assert dist((7, 8), (10, 2)) == 9


def test_row_intersect():
    row = 10
    sensor = Sensor(
        pos=(7, 8),
        beacon=(10, 2)
    )
    assert row_intersect(row, sensor) == (2, 14)


def test_first():
    assert first(io.StringIO(data), 10) == 26


def test_second():
    assert second(io.StringIO(data), 20) == 56000011
