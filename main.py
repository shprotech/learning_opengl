"""
Main entry point for the application.

:author: shaharmelamed
:date: 17/03/2024
"""
import math
import sys

import numpy as np
from OpenGL import GL, GLU, GLUT

import handle_inputs
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, WORLD_MIN_X, WORLD_MAX_X, WORLD_MIN_Y, WORLD_MAX_Y


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


def display_sinus():
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)

    GL.glViewport(
        0,
        0,
        math.floor(.8 * window_width),
        math.floor(.8 * window_height)
    )
    GL.glBegin(GL.GL_LINE_STRIP)
    for x in np.arange(-4., 4., 0.01):
        y = np.sin(x)
        GL.glVertex2f(x, y)

    GL.glEnd()

    GL.glViewport(
        math.floor(.8 * window_width),
        math.floor(.8 * window_height),
        math.floor(.2 * window_width),
        math.floor(.2 * window_height)
    )
    GL.glBegin(GL.GL_LINE_STRIP)
    for x in np.arange(-4., 4., 0.01):
        y = np.sin(x)
        GL.glVertex2f(x, y)

    GL.glEnd()

    GL.glFlush()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glColor3f(0.0, 0.4, 0.2)

    display_sinus()

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
