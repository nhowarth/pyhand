# CIS 192 - Python Final Project
# Wireframe Hand Model
# Nick Howarth <nhowarth>
# References:
### http://codentronix.com/2011/04/20/simulation-of-3d-point-rotation-with-python-and-pygame/
### http://pygame.org/docs

import sys
import math
import pygame
import csv
from pygame.locals import *
from nose.tools import eq_


def slicer(all_points, ppf):
    """Breaks all_points (list of points) into frames
    of size ppf (points per frame). Returns list of frames."""
    return (all_points[i:i + ppf] for i in xrange(0, len(all_points), ppf))


def test_slicer():
    """Function to validate operation of slicer."""
    point_list = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3,
                  4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7]
    for slice_size in (4, 8, 16, 32):
        for frame in slicer(point_list, slice_size):
            eq_(len(frame), slice_size,
                msg="slicer returns list of wrong size")


class InvalidInputFile(Exception):
    """Invalid input file format."""
    pass


def cos_and_sin(angle):
    """Converts angle given in degrees to angle in radians,
    and returns tuple containing cos(angle) and sin(angle).
    >>> cos_and_sin(0)
    (1.0, 0.0)
    >>> cos_and_sin(90)
    (6.123031769111886e-17, 1.0)
    """
    rad = angle * math.pi / 180
    return (math.cos(rad), math.sin(rad))


class Point3D:
    """Initializes point in 3-dimensional space."""
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """Rotates point around x-axis by angle given in degrees."""
        (cosa, sina) = cos_and_sin(angle)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """Rotates point around y-axis by angle given in degrees."""
        (cosa, sina) = cos_and_sin(angle)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """Rotates point around z-axis by angle given in degrees."""
        (cosa, sina) = cos_and_sin(angle)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, vision_field=512, viewer_dist=5):
        """Uses perspective projection to transforms 3D point to 2D.
        vision_field (field of vision parameter) and viewer_dist ("distance"
        from viewer to point) are optimized for hand.txt sample.
        Tune as needed."""
        factor = vision_field / (viewer_dist + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)


class Simulation:
    def __init__(self, win_width=640, win_height=480):
        """Initialization of pygame environment and hand joint coordinates."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("3D Wireframe Hand Model Simulation")

        # Read in joint positions from csv file (argument from command line).
        self.joints = []
        with open(sys.argv[1], 'rU') as f:
            csvf = csv.reader(f)
            for line in csvf:
                try:
                    self.joints.append(Point3D(line[0], line[1], line[2]))
                except IndexError:
                    raise InvalidInputFile("Each line must have following \
                                            format:  'x, y, z'")
        if len(self.joints) % 21 != 0:
            raise InvalidInputFile("Total number of lines in input file must \
                                    be a multiple of 21.")

        # Define the points that compose each of the fingers.
        self.index = (0, 1, 2, 3, 19)
        self.middle = (4, 5, 6, 7, 19)
        self.ring = (8, 9, 10, 11, 19)
        self.pinky = (12, 13, 14, 15, 19)
        self.thumb = (16, 17, 18, 19, 20)

        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        self.play = 0

    def run(self):
        """Loop that animates hand movement."""
        while 1:
            # Only look at 21 joint positions at a time.
            for frame in slicer(self.joints, 21):
                # Stay on first frame if not in play mode.
                if self.play == 0:
                    frame = self.joints[0:21]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                self.clock.tick(5)  # frames per second
                self.screen.fill((0, 0, 0))  # clear screen

                j2D = []  # Holds transformed (2D) joint positions.

                for joint in frame:
                    # Rotate point around x-axis, then y-axis, then z-axis.
                    Rotated = joint.rotateX(self.angleX).rotateY(self.angleY)\
                                   .rotateZ(self.angleZ)
                    # Transform the point from 3D to 2D.
                    Projected = Rotated.project(self.screen.get_width(),
                                                self.screen.get_height())
                    # Add the projected point to list of 2D points.
                    j2D.append(Projected)

                # Define fingers
                index = self.index
                middle = self.middle
                ring = self.ring
                pinky = self.pinky
                thumb = self.thumb

                # Draw fingers
                pygame.draw.lines(self.screen, (255, 100, 200), False,
                                  [(j2D[index[0]].x, j2D[index[0]].y),
                                   (j2D[index[1]].x, j2D[index[1]].y),
                                   (j2D[index[2]].x, j2D[index[2]].y),
                                   (j2D[index[3]].x, j2D[index[3]].y),
                                   (j2D[index[4]].x, j2D[index[4]].y)], 4)
                pygame.draw.lines(self.screen, (255, 0, 0), False,
                                  [(j2D[middle[0]].x, j2D[middle[0]].y),
                                   (j2D[middle[1]].x, j2D[middle[1]].y),
                                   (j2D[middle[2]].x, j2D[middle[2]].y),
                                   (j2D[middle[3]].x, j2D[middle[3]].y),
                                   (j2D[middle[4]].x, j2D[middle[4]].y)], 4)
                pygame.draw.lines(self.screen, (0, 0, 255), False,
                                  [(j2D[ring[0]].x, j2D[ring[0]].y),
                                   (j2D[ring[1]].x, j2D[ring[1]].y),
                                   (j2D[ring[2]].x, j2D[ring[2]].y),
                                   (j2D[ring[3]].x, j2D[ring[3]].y),
                                   (j2D[ring[4]].x, j2D[ring[4]].y)], 4)
                pygame.draw.lines(self.screen, (255, 200, 0), False,
                                  [(j2D[pinky[0]].x, j2D[pinky[0]].y),
                                   (j2D[pinky[1]].x, j2D[pinky[1]].y),
                                   (j2D[pinky[2]].x, j2D[pinky[2]].y),
                                   (j2D[pinky[3]].x, j2D[pinky[3]].y),
                                   (j2D[pinky[4]].x, j2D[pinky[4]].y)], 4)
                pygame.draw.lines(self.screen, (0, 255, 0), False,
                                  [(j2D[thumb[0]].x, j2D[thumb[0]].y),
                                   (j2D[thumb[1]].x, j2D[thumb[1]].y),
                                   (j2D[thumb[2]].x, j2D[thumb[2]].y),
                                   (j2D[thumb[3]].x, j2D[thumb[3]].y),
                                   (j2D[thumb[4]].x, j2D[thumb[4]].y)], 4)

                for r in range(0, 10):
                # Rotate around axis if specific key pressed.
                # For loop used to increase rate of rotation without
                # affecting update rate of joint positions.
                    if pygame.key.get_pressed()[K_u]:
                        self.angleX += 1
                    if pygame.key.get_pressed()[K_n]:
                        self.angleX -= 1
                    if pygame.key.get_pressed()[K_h]:
                        self.angleY += 1
                    if pygame.key.get_pressed()[K_l]:
                        self.angleY -= 1
                    if pygame.key.get_pressed()[K_j]:
                        self.angleZ += 1
                    if pygame.key.get_pressed()[K_k]:
                        self.angleZ -= 1
                    # Start animation if space bar is pressed
                    # (if not started already).
                    if pygame.key.get_pressed()[K_SPACE]:
                        self.play = 1

                # Update the full display surface to the screen
                pygame.display.flip()

            # Reset play mode to 0 after one animation cycle
            # Only plays after space bar is pressed
            self.play = 0


def main():
    """Main function. Runs the doctests, nosetests, and simulation."""
    import doctest
    options = (doctest.IGNORE_EXCEPTION_DETAIL | doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS)
    doctest.testmod(optionflags=options)

    print "\nRunning unit tests...\n"
    import nose
    if nose.run(argv=["--with-coverage", "pyhand.py"]):
        print "\nPassed all unit tests"

    Simulation().run()


if __name__ == "__main__":
    main()
