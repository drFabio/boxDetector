from unittest import TestCase
from boxDetector.lineSegment import LineSegment

from boxDetector.checkBoxDetector import(
    LineGroup,
    flatten_line_segment
)


class TestFlattenLineSegment(TestCase):

    def test_join_same_level(self):
        a = LineSegment((0, 0), (1, 1))
        b = LineSegment((2, 2), (3, 3))
        c = LineSegment((5, 5), (10, 10))
        flatten = flatten_line_segment([a,b,c],a.unit_vector)
        joined = flatten[0.0]
        self.assertEqual(joined.a, (0, 0))
        self.assertEqual(joined.b, (10, 10))

    def test_join_varying_level(self):
        a = LineSegment((0, 0), (0, 1))
        b = LineSegment((0, 2), (0, 5))
        c = LineSegment((15, 2), (15, 10))
        flatten = flatten_line_segment([a,b,c],a.unit_vector,gap_epsilon=6)
        # CHecking it respected the levels erasing the merged ones
        self.assertIn(0.0, flatten)
        self.assertNotIn(3.0, flatten)
        self.assertIn(15.0, flatten)
        joined = flatten[0.0]
        self.assertEqual(joined.a, a.a)
        self.assertEqual(joined.b, b.b)
        self.assertEqual(flatten[15.0], c)
