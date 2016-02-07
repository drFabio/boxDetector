## The problem.

Detect checkboxes using openCV

## The solution.

First we find all closed contours using findContours and then checking on hierarchy if it has a chield hierarchy[i][2] != -1
After that we check if the child hierarchy has a sibling (otherwise it's just the internal contour and the contour is not filled)
firtstChildHierarchy = hierarchy[hierarchy[i][2]]
isFilled = firtstChildHierarchy[0]!=-1
After that we check if it resembles a box by having 2 sets of parallel lines perpendicular with each other
