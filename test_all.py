from days import day_1_1, day_1_2
from days import day_2_1, day_2_2
from days import day_3_1, day_3_2
from days import day_4_1, day_4_2
from days import day_5_1, day_5_2
from days import day_6_1, day_6_2


def test_1_1():
    assert day_1_1.run() == 866436


def test_1_2():
    assert day_1_2.run() == 276650720


def test_2_1():
    assert day_2_1.run() == 483


def test_2_2():
    assert day_2_2.run() == 482


def test_3_1():
    assert day_3_1.run() == 299


def test_3_2():
    assert day_3_2.run() == 3621285278


def test_4_1():
    assert day_4_1.run() == 242


def test_4_2():
    assert day_4_2.run() == 186


def test_5_1():
    assert day_5_1.run() == 926


def test_5_2():
    assert day_5_2.run() == 657


def test_6_1():
    assert day_6_1.run() == 6443


def test_6_2():
    assert day_6_2.run() == 3232
