"""
Handle inputs from the user.

:author: shaharmelamed
:date: 17/03/2024
"""
import random
import os

from OpenGL import GL, GLU, GLUT

from consts import WORLD_MIN_X, WORLD_MAX_X, WORLD_MIN_Y, WORLD_MAX_Y

type Coordinate = tuple[float, float]


PROVIDED_COORDINATES: list[Coordinate] = []


def convert_to_world_coordinates(x: int, y: int) -> Coordinate:
    """
    Convert screen coordinates to world coordinates.

    This function takes in screen coordinates (x, y) and converts them to world coordinates.
    The conversion is done based on the current window's width and height.

    :param x: The x-coordinate on the screen.
    :param y: The y-coordinate on the screen.
    :return: A tuple containing the converted x and y coordinates in the world coordinate system.
    """
    # Get the current window's width
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    # Get the current window's height
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)

    # Convert the x-coordinate from screen to world
    x = (x / window_width) * (WORLD_MAX_X - WORLD_MIN_X) + WORLD_MIN_X
    # Convert the y-coordinate from screen to world
    y = ((window_height - y) / window_height) * (WORLD_MAX_Y - WORLD_MIN_Y) + WORLD_MIN_Y

    # Return the converted coordinates
    return x, y


def set_random_draw_color():
    """
    Set the drawing color to a random color.

    This function sets the drawing color to a random color.
    """
    # Generate a random color
    r = random.random()
    g = random.random()
    b = random.random()

    # Set the drawing color to the random color
    GL.glColor3f(r, g, b)


def mouse(button: int, state: int, mouse_x: int, mouse_y: int):
    """
    Handle mouse events.

    This function is called when a mouse event occurs. It handles left and right mouse button events.
    When the left mouse button is pressed, it sets a random draw color and draws a point at the mouse position.
    When the right mouse button is released, it clears the color buffer bit.

    :param button: The button on the mouse that was pressed or released.
    :param state: The state of the button (pressed or released).
    :param mouse_x: The x-coordinate of the mouse cursor.
    :param mouse_y: The y-coordinate of the mouse cursor.
    """
    # Get the current window's width
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    # Get the current window's height
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)

    # Convert the mouse coordinates from screen to world
    world_x, world_y = convert_to_world_coordinates(mouse_x, mouse_y)

    # If the left mouse button is pressed
    if button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN:
        # Set a random draw color
        set_random_draw_color()

        # Set the viewport to the entire window
        GL.glViewport(
            0,
            0,
            window_width,
            window_height
        )

        PROVIDED_COORDINATES.append((world_x, world_y))

        # Start drawing points
        GL.glBegin(GL.GL_LINE_STRIP)

        for x, y in PROVIDED_COORDINATES:
            GL.glVertex2f(x, y)

        # End drawing points
        GL.glEnd()
    # If the right mouse button is released
    elif button == GLUT.GLUT_RIGHT_BUTTON and state == GLUT.GLUT_UP:
        # Clear the color buffer bit
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    # Flush all drawing commands and swap the buffers
    GL.glFlush()


def keyboard(key: bytes, x: int, y: int):
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)
    world_x, world_y = convert_to_world_coordinates(x, y)
    GL.glViewport(0, 0, window_width, window_height)

    set_random_draw_color()

    GL.glRasterPos2f(world_x, world_y)
    GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_18, ord(key))
    GL.glFlush()
