#! /usr/bin/env python3
"""Box detector
    This module  has functions to determine if a contour ressembles a box

    A box is considered something that has 2 sets of paralel  line segments,
    perpendicular to each other and each paralel segment is roughly
    the same size
"""
from collections import namedtuple
from boxDetector.lineSegment import LineSegment as Segment
import numpy as np
import cv2

LineGroup = namedtuple("LineGroup", "norm pivotPoint lines")
Checkbox = namedtuple("Checkbox", "a b c d")

def build_segments_angle_map(points, angle_precision=4, min_size=5):
    """ Given a list of points build a line segment list

    All segments are compared to [0,1] and it's angle is used as key
    The vector of the 1st segment on a angle becames the pivotPoint
    all angles are indexed by distance with the pivot

    Args:
        points (List[Tuple(int,int)]): list of points on contour
        angle_precision (int): decimal point precision,defaults to 4
        min_size (int) : minimun segment size to consider
    """

    def add_segment(segment,angle_map):
        angle = segment.get_angle()
        angle = round(angle, angle_precision)
        if angle in angle_map:
            angle_map[angle].lines.append(segment)
        else:
            norm = segment.unit_vector
            pivotPoint = segment.vector
            angle_map[angle] = LineGroup(
                norm, pivotPoint, [segment])

    angle_segment_map = dict()
    ref_point = points[0]
    to_add = False
    segment = None
    # Indexing all line segments by angle in relation to a randle vector
    for i in range(1, len(points)):
        next_point = points[i]
        segment = Segment(
            ref_point, next_point, angle_precision=angle_precision)
        if segment.length < min_size:
            to_add = True
            continue
        to_add = False
        ref_point = next_point
        add_segment(segment,angle_segment_map)
    if to_add:
        add_segment(segment,angle_segment_map)
    return angle_segment_map


def getRadAngle(degreeAngle):
    radAngle = (degreeAngle*np.pi)/180
    return round(radAngle, 4)

def flatten_angles(angle_map, rad_angle_epsilon=8):
    """Concat similar angles together
    Args:
        angle_map (dict): list of something indexed by angles
        rad_angle_epsilon (float): how much of the difference to squash in rad
    """
    ret = {}
    last_angle = None

    for angle in sorted(angle_map):
        if last_angle is None:
            last_angle = angle
        if angle - last_angle > rad_angle_epsilon:
            last_angle = angle
        if last_angle in ret:
            current_lines = angle_map[angle].lines
            norm = ret[last_angle].norm
            for segment in current_lines:
                projected = segment.get_projected_segment(norm)
                ret[last_angle].lines.append(projected)
        else:
            ret[last_angle] = angle_map[angle]
    return ret


def flatten_line_segment(segments,norm, gap_epsilon=10):
    """Join multiple distance segments that are on the same gap_epsilon
    Args:
        segments (List): List of all segments
        gap_epsilon: what is the gap_epsilon to merge
    """
    def get_distance(point,norm):
        return abs(np.cross(norm,point))

    dist_dict = {}
    last_distance = None
    distance_segment_map = {}
    segments.sort()
    base = segments[0]
    for i in range(1, len(segments)):
        segment = segments[i]
        gap = [base.b[0]-segment.a[0], base.b[1]-segment.a[1]]
        dist = (gap[0]**2+gap[1]**2)**0.5
        if dist < gap_epsilon:
            base.add_segment(segment)
        else:
            distance = get_distance(base.a,norm)
            dist_dict[distance] = base
            base = segment
    distance = get_distance(base.a,norm)
    dist_dict[distance] = base
    return dist_dict

def is_boxy(points, angle_epsilon=8, parallel_epsilon=0.5, min_size=5, gap_epsilon=10):
    """Wheter a point set resemble a box
    Args:
        angle_epsilon: angle diff that can be merged
        parallel_epsilon: how much can parallel lines differ
        min_size: min size that a segment must have
        gap_epsilon: min gap before merging segments
    """
    angle_epsilon = getRadAngle(angle_epsilon)

    angle_map = build_segments_angle_map(points, min_size=min_size)
    flatted = flatten_angles(angle_map, rad_angle_epsilon=angle_epsilon)
    ninety_degree = np.pi/2
    angles_to_check = []

    for angle in flatted:
        flated_lines = flatten_line_segment(
            flatted[angle].lines,flatted[angle].norm, gap_epsilon=gap_epsilon)
        has_parallel = False
        length_to_compare = None
        for distance in flated_lines:
            if flated_lines[distance].length < min_size:
                continue
            if not length_to_compare:
                length_to_compare = flated_lines[distance].length
            else:
                size_diff = 0.0
                if length_to_compare > flated_lines[distance].length:
                    size_diff = flated_lines[distance].length/length_to_compare
                else:
                    size_diff = length_to_compare/flated_lines[distance].length
                    length_to_compare = flated_lines[distance].length
                if (1-size_diff) < parallel_epsilon:
                    has_parallel = True
                    break

        if has_parallel:
            angles_to_check.append(angle)
    for angle in angles_to_check:
        start = 1
        for i, next_angle in enumerate(angles_to_check, start):
            if (ninety_degree-angle_epsilon) <= abs(angle-next_angle) <= (ninety_degree+angle_epsilon):
                return True
        start += 1
    return False

def formatBox(box):
    ret =[]
    for item in box:
        ret.append((item[0].item(),item[1].item()))
    return ret

def get_filled_contours(img_path,min_rect_size = 30):
    filled_coordinates = []
    img = cv2.imread(img_path)
    #Make it gray
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #reducing noise
    ret,thresh = cv2.threshold(imgray,127,255,0)
    _,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #hierarchy fix and skipping outer container
    hierarchy = hierarchy[0][1:]
    #the first one is always the outer container skipping it 
    contours = contours[1:]
    for i,cnt in enumerate(contours):
            #[0] = next contour at the same hierarchical level
            #[1] = previous contour at the same hierarchical level
            #[2] = denotes its first child contour
            #[3] = denotes index of its parent contour
            child_index = hierarchy[i][2]
            isClosedShape = child_index != -1
            if isClosedShape:
                # -1 because we skipped the outer contour
                firtstChildHierarchy = hierarchy[child_index-1]
                isFilled = firtstChildHierarchy[0]!=-1
                if isFilled:
                    #Finds the minimun area rectangle for the contour
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    width = box[3][0] - box[0][0]
                    if width< min_rect_size:
                        continue
                    contour_list=list(map(lambda x: x[0], cnt))
                    if not is_boxy(contour_list):
                        continue
                    filled_coordinates.append(formatBox(box))                 
    return filled_coordinates