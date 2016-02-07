import math
from unittest import TestCase
from boxDetector.lineSegment import LineSegment
from boxDetector.checkBoxDetector import build_segments_angle_map

ninety_degrees = round(math.pi/2, 4)


class TestAngleMap(TestCase):

    def setUp(self):
        self.perfect_5_box = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]

    def test_angle_indexing(self):
        angle_map = build_segments_angle_map(self.perfect_5_box)
        print(angle_map.keys())
        self.assertEqual(len(angle_map.keys()), 2)
        self.assertIn(ninety_degrees, angle_map)
        self.assertIn(0.0, angle_map)

    def test_segment_indexing(self):
        points = self.perfect_5_box
        angle_map = build_segments_angle_map(points)

        zero_segments = angle_map[0.0]
        # Checking if the pivot point is the first vector
        segment = LineSegment(points[0], points[1])
        self.assertEqual(zero_segments.pivotPoint, segment.vector)
        self.assertEqual(zero_segments.norm, segment.unit_vector)
        lines = zero_segments.lines
      
        self.assertIn(segment,lines)
        segment = LineSegment(points[2], points[3])
        self.assertIn(segment,lines)

        ninety_segments = angle_map[ninety_degrees]
        segment = LineSegment(points[1], points[2])
        self.assertEqual(ninety_segments.pivotPoint, segment.vector)
        self.assertEqual(ninety_segments.norm, segment.unit_vector)
        lines = ninety_segments.lines
        self.assertIn(segment,lines)
        segment = LineSegment(points[3], points[4])
        self.assertIn(segment,lines)


    def test_segment_skiping(self):
        """
            Check if segments less than min are skipped until min is reached
        """
        points = [(0, 0), (2, 0), (5, 0)]
        angle_map = build_segments_angle_map(points, min_size=5)
        self.assertIn(0.0, angle_map)
        segment = LineSegment(points[0], points[2])
        lines = angle_map[0.0].lines
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], segment)
