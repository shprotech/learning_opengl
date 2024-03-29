"""
Main entry point for the application.

:author: shaharmelamed
:date: 17/03/2024
"""
import math
import sys
from contextlib import contextmanager

import numpy as np
from OpenGL import GL, GLU, GLUT

import handle_inputs
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, WORLD_MIN_X, WORLD_MAX_X, WORLD_MIN_Y, WORLD_MAX_Y

type Vertex3D = np.ndarray


@contextmanager
def gl_draw(mode: int):
    """
    Context manager for OpenGL drawing.

    This context manager is used to encapsulate OpenGL drawing code.
    It starts the drawing mode and ends it when the block is exited.

    :param mode: The OpenGL drawing mode to use.
    """
    GL.glBegin(mode)
    try:
        yield
    finally:
        GL.glEnd()


def init_glut():
    GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutInitWindowPosition(50, 100)

    GLUT.glutInit(*sys.argv)
    GLUT.glutCreateWindow("OpenGL Window")


def init():
    GL.glClearColor(1.0, 1.0, 1.0, 0.0)
    GL.glColor3f(0.0, 0.0, 0.0)
    GL.glPointSize(4.0)

    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluOrtho2D(WORLD_MIN_X, WORLD_MAX_X, WORLD_MIN_Y, WORLD_MAX_Y)


def register_callbacks():
    GLUT.glutDisplayFunc(display)
    GLUT.glutMouseFunc(handle_inputs.mouse)
    GLUT.glutKeyboardFunc(handle_inputs.keyboard)


def display_quads():
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)

    GL.glViewport(
        0,
        0,
        math.floor(window_width),
        math.floor(window_height)
    )
    with gl_draw(GL.GL_QUAD_STRIP):
        GL.glVertex2f(-2, 0)  # 1
        GL.glVertex2f(-2 + 1.1547005383792517, -2)  # 2
        GL.glVertex2f(0, -2.5)  # 2.5
        GL.glVertex2f(2.3094010767585034 + -2 + 1.1547005383792517, -2)  # 3
        GL.glVertex2f(2.3094010767585034 + -2 + 1.1547005383792517 + 1.1547005383792517, 0)  # 4
        GL.glVertex2f(2.3094010767585034 + -0.8452994616207483, 2)  # 5
        GL.glVertex2f(0, 2.3)  # 5.5
        GL.glVertex2f(-0.8452994616207483, 2)  # 6

    GL.glFlush()


def rotate_vertex_around_x(vertex: Vertex3D, angle: float) -> Vertex3D:
    # Rotation matrix around the x-axis
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])
    return np.dot(rotation_matrix, vertex)


def rotate_vertex_around_y(vertex: Vertex3D, angle: float) -> Vertex3D:
    # Rotation matrix around the y-axis
    rotation_matrix = np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])
    return np.dot(rotation_matrix, vertex)


def display_cube():
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)

    GL.glViewport(
        0,
        0,
        math.floor(window_width),
        math.floor(window_height)
    )
    points: list[Vertex3D] = [
        np.array([0, 0, 0]),
        np.array([0, 1, 0]),
        np.array([1, 0, 0]),
        np.array([1, 1, 0]),
        np.array([0, 0, 1]),
        np.array([0, 1, 1]),
        np.array([1, 0, 1]),
        np.array([1, 1, 1]),
    ]
    # Rotate each point by 45 degrees around the y-axis
    points = [rotate_vertex_around_y(point, math.radians(45)) for point in points]
    # Rotate each point by 45 degrees around the x-axis
    points = [rotate_vertex_around_x(point, math.radians(45)) for point in points]

    GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
    GL.glVertexPointer(3, GL.GL_FLOAT, 0, np.array(points, dtype=np.float32))
    vert_index = np.array([
        6, 2, 3, 7,
        5, 1, 0, 4,
        7, 3, 1, 5,
        4, 0, 2, 6,
        2, 0, 1, 3,
        7, 5, 4, 6
    ])
    GL.glDrawElements(GL.GL_QUADS, 24, GL.GL_UNSIGNED_INT, vert_index)
    GL.glDisableClientState(GL.GL_VERTEX_ARRAY)

    GL.glFlush()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glColor3f(0.0, 0.4, 0.2)

    display_cube()

    print_gl_error()


def print_gl_error():
    error = GL.glGetError()
    if error != GL.GL_NO_ERROR:
        print(f"OpenGL error: {error}")
    else:
        print("OpenGL error: no error")


def main():
    init_glut()
    init()
    register_callbacks()
    GLUT.glutMainLoop()


if __name__ == '__main__':
    main()
