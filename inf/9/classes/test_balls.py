from ball import Scene, Ball, Coordinate, Artist, Shape, BoundingBox, Crossing

import pytest, random


@pytest.fixture
def random_coord():
    return Coordinate(random.randint(0, 256),
                      random.randint(0, 256))


def test_coord(random_coord):
    
    f = random.random() * -1.0
    c2 = random_coord * f
    assert c2.x <= 0
    assert c2.y <= 0


def test_bbox():
    box = BoundingBox(
        top=random.randint(-256,256),
        left=random.randint(-256,256),
        bottom=random.randint(-256,256),
        right=random.randint(-256,256)
    )

    for i in range(1000):
        s1 = Coordinate(random.randint(box.right,  box.right+1000),
                        random.randint(box.bottom, box.bottom+1000))

        c = box.crosses(s1)
        print(c, box, s1)
        assert Crossing.Right in c
        assert Crossing.Bottom in c


