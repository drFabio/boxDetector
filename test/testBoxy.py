from unittest import TestCase
from boxDetector.lineSegment import LineSegment

from boxDetector.checkBoxDetector import(
    LineGroup,
    minRadAngle,
    is_boxy
)

class TestBoxy(TestCase):
    def setUp(self):
        self.perfect_box = [(0,0),(0,10),(10,10),(10,0),(0,0)]
        self.box_with_noise = [(0,0),(1,1),(2,2),(0,2),(0,10),(10,10),(10,0),(0,0)]
        self.open = [(0,0),(1,1),(2,2),(0,10),(10,10)]

    def test_perfect_box(self):
        self.assertTrue(is_boxy(self.perfect_box))

    def test_noise(self):
        self.assertTrue(is_boxy(self.box_with_noise))

    def test_open(self):
        self.assertFalse(is_boxy(self.open))