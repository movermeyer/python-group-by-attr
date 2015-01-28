from collections import namedtuple
from nose.tools import eq_, raises
from group_by_attr import group_by_attr


#
# Tests
#

def test_group_by_attr():
    test_scenario = namedtuple('test_scenario', (
        'attr',
        'expected_result'))

    a, b, c = (
        Struct(x=1, y=1, z=1),
        Struct(x=1, y=2, z=2),
        Struct(x=1, y=1, z=3))

    scenarios = (
        test_scenario(attr='x', expected_result={
            1: (a, b, c)}),
        test_scenario(attr='y', expected_result={
            1: (a, c),
            2: (b,)}),
        test_scenario(attr='z', expected_result={
            1: (a,),
            2: (b,),
            3: (c,)}))

    def assert_group_by_attr(scenario):
        eq_(group_by_attr(attr=scenario.attr, items=(a, b, c)),
            scenario.expected_result)

    for s in scenarios:
        yield assert_group_by_attr, s


def test_custom_getattr_fn():
    a, b, c = {'x': 1}, {'x': 2}, {'x': 1}

    actual_result = group_by_attr(
        attr='x',
        items=(a, b, c),
        getattr_fn=dict.__getitem__)

    eq_(actual_result, {
        1: (a, c),
        2: (b,)})


@raises(AttributeError)
def test_missing_attribute():
    group_by_attr(attr='missing', items=(Struct(x=0, y=0, z=0),))


#
# Test Helpers
#

Struct = namedtuple('Struct', ('x', 'y', 'z'))
