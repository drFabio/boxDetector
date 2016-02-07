from unittest import TestCase
from boxDetector.lineSegment import LineSegment

from boxDetector.checkBoxDetector import(
    LineGroup,
    minRadAngle,
    flatten_angles
)

class TestFlattenAngle(TestCase):

    def test_angle_flatten(self):
        def check_seg_in_list(angle, flatten, to_check):
            segments = flatten[angle].lines
            projected = to_check.get_projected_segment(flatten[angle].norm)
            for segment in segments:
                if projected == segment:
                    return True
            return False
        angleDict = {}
        segments = []
        for i in range(0, 16, 2):
            segments.append(LineSegment((i, i), (i+1, i+1)))

        uv = segments[0].unit_vector
        lines = [segments[0],segments[1]]
        ok = LineGroup(uv, None, segments)
        angle_ok = 0.0
        angleDict[angle_ok] = ok

        uv = segments[2].unit_vector
        lines = [segments[2],segments[3]] 
        to_flat = LineGroup(uv, None, lines)
        angle_flatten = angle_ok+minRadAngle
        angleDict[angle_flatten] = to_flat

        uv = segments[4].unit_vector
        lines = [segments[4],segments[5]] 
        ok2 = LineGroup(uv, None, lines)
        angle_ok_2 = angle_flatten+0.1
        angleDict[angle_ok_2] = ok2

        uv = segments[6].unit_vector
        lines = [segments[6],segments[7]] 
        not_flatten = LineGroup(uv, None, lines)

        angle_not_flatten = angle_ok_2+minRadAngle+0.2
        angleDict[angle_not_flatten] = not_flatten
        flatten = flatten_angles(angleDict)

        self.assertNotIn(angle_flatten, flatten)
        self.assertIn(angle_ok, flatten)
        self.assertIn(angle_ok_2, flatten)
        self.assertIn(angle_not_flatten, flatten)

        to_check = flatten[angle_ok].lines
        self.assertIn(ok.lines[0], to_check)

        segment = to_flat.lines[0]
        self.assertTrue(check_seg_in_list(angle_ok, flatten, segment))
        self.assertIn(ok.lines[0], to_check)
        segment = to_flat.lines[1]
        self.assertTrue(check_seg_in_list(angle_ok,flatten, segment))

        to_check = flatten[angle_ok_2].lines
        self.assertIn(ok2.lines[0], to_check)
        self.assertIn(ok2.lines[1], to_check)

        to_check = flatten[angle_not_flatten].lines
        self.assertIn(not_flatten.lines[0], to_check)
        self.assertIn(not_flatten.lines[1], to_check)
