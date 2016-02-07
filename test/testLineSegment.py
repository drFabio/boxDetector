import math
from unittest import TestCase
from boxDetector.lineSegment import LineSegment


class TestLineSegment(TestCase):

    def test_right_order(self):
        """
        Test that a line segment instantiate the original order if both A and B are on the right orer
        """
        segment = LineSegment((0, 0), (5, 0))
        self.assertEqual(segment.a, (0, 0))
        self.assertEqual(segment.b, (5, 0))

    def test_A_x_after(self):
        """
        Test that a line segment instantiate the inverser order if A.x is after b 
        """
        a = (1, 0)
        b = (0, 0)
        segment = LineSegment(a, b)
        self.assertEqual(segment.a, b)
        self.assertEqual(segment.b, a)

    def test_A_y_after(self):
        """
        Test that a line segment instantiate the inverser order if A.x is after b 
        """
        a = (0, 1)
        b = (0, 0)
        segment = LineSegment(a, b)
        self.assertEqual(segment.a, b)
        self.assertEqual(segment.b, a)

    def test_vector_creation(self):
        """
        Test if the vetor is actualy created
        """
        a = (1, 1)
        b = (10, 2)
        segment = LineSegment(a, b)
        vector = [b[0]-a[0], b[1]-a[1]]
        self.assertEqual(segment.x, vector[0])
        self.assertEqual(segment.y, vector[1])
        length = (vector[0]**2 + vector[1]**2)**0.5
        self.assertEqual(segment.length, length)

    def test_unit_vector(self):
        """
        Test that a line segment makes the right unit vector
        """
        a = (0, 5)
        b = (10, 10)
        segment = LineSegment(a, b)
        unit = [segment.x/segment.length, segment.y/segment.length]
        self.assertEqual(segment.unit_vector, unit)

    def test_default_angle(self):
        """
        The angle shold by default test the vector with (1,0)
        """
        a = (0, 0)
        b = (0, 10)
        segment = LineSegment(a, b)
        angle = segment.get_angle()
        expected_angle = round(math.pi/2, segment.angle_precision)
        self.assertEqual(angle, expected_angle)

    def test_add_segment_before(self):
        a = (5, 5)
        b = (10, 10)
        c = (0, 0)
        d = (4, 4)
        segment = LineSegment(a, b)
        to_add = LineSegment(c, d)
        segment.add_segment(to_add)
        self.assertEqual(segment.a, c)
        self.assertEqual(segment.b, b)

    def test_add_segment_after(self):
        c = (5, 5)
        d = (10, 10)
        a = (0, 0)
        b = (4, 4)
        segment = LineSegment(a, b)
        to_add = LineSegment(c, d)
        segment.add_segment(to_add)
        self.assertEqual(segment.a, a)
        self.assertEqual(segment.b, d)

    def test_add_segment_middle(self):
        a = (0, 0)
        b = (10, 10)
        c = (2, 2)
        d = (4, 4)
        segment = LineSegment(a, b)
        to_add = LineSegment(c, d)
        segment.add_segment(to_add)
        self.assertEqual(segment.a, a)
        self.assertEqual(segment.b, b)
