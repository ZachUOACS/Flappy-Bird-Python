"""
Flappy bird game.

A game where you control a bird that has to go through sets of pipes,
each time the bird goes through a pipe you get one score.

You control the bird by pressing the space bar,
when you press space bar the bird will 'flap' up.
The bird is affected by gravity,
so you will need make the bird flap through the pipes

Made by Zach
"""
from tkinter import *
from random import *


class GUI:
    """
    This class creates a GUI that displays the game and runs the game.

    creates start screen bird and pipe when constructed

    Attributes
    ----------
    _window : tk window
        A window that allows the game to be created on
    _canvas : tk canvas
        A canvas that displays the game,
        the bird and pipe are created on the canvas
    _bird : Bird instance
        Creates an instance of a bird that the player can control
    _pipe : Pipe instance
        Creates an instance of a pipe
    _reset_button : tk button
        A button that can reset the game
    _exit_button : tk button
        A button that can exit the game
    _score : int
        The players score
    _score_text : canvas text
        A text that displays the players score
    _hs : int
        The players high score
    _play_button : tk button
        A button that starts the game

    """

    CANVAS_HEIGHT = 700
    CANVAS_WIDTH = 700
    PADDING = 50
    _FLAP_HEIGHT = -14
    _BUTTON_WIDTH = 15
    _REFRESH_RATE = int(1000/60)
    _TEXT_PADDING = 10

    def __init__(self):
        """
        Construct all necessary attributes for the GUI.

        Also displays start screen.
        """
        # Create window
        self._window = Tk()
        self._window.title(string="Flappy bird")

        # Creating and placing canvas
        self._canvas = Canvas(self._window, width=GUI.CANVAS_WIDTH,
                              height=GUI.CANVAS_HEIGHT, background="#00C0F0")
        self._canvas.grid(row=0, column=0)

        # Creating bird
        self._bird = Bird(self._canvas)

        # Creating pipe
        self._pipe = Pipe(self._canvas)

        # binds space to flap
        self._window.bind("<space>", self._flap)

        # Reset Button
        self._reset_button = Button(self._window, text="Play Again",
                                    command=self._reset_game,
                                    width=GUI._BUTTON_WIDTH,
                                    activebackground="green")

        # Exit button
        self._exit_button = Button(self._window, text="Exit",
                                   command=exit, width=GUI._BUTTON_WIDTH,
                                   activebackground="red")

        # Score
        self._score = 0
        # High score
        self._hs = 0

        # Score text
        self._score_text = self._canvas.create_text(GUI.CANVAS_WIDTH/2,
                                                    GUI.PADDING,
                                                    fill="white",
                                                    font="System 40 bold",
                                                    text=self._score)

        # Start Screen
        # Disable 'space' for start screen
        # and 'Alt' and 'F10' to stop the game pausing
        self._window.unbind_class("Button", "<Key-space>")
        self._window.unbind_all("<Alt_L>")
        self._window.unbind_all("<Alt_R>")
        self._window.unbind_all("<F10>")
        # Start button
        self._play_button = Button(self._window, text="Click to play",
                                   command=self._start_game,
                                   width=GUI._BUTTON_WIDTH,
                                   activebackground="green")
        # Place start button
        self._play_button.place(x=(self.CANVAS_WIDTH/2) - GUI.PADDING,
                                y=self.CANVAS_HEIGHT/2)

        # Title
        self._canvas.create_text(GUI.CANVAS_WIDTH/2,
                                 GUI.CANVAS_HEIGHT/2 -
                                 (GUI.PADDING * 2),
                                 fill="white", font="System 40 bold",
                                 text="Flappy Bird", tags="start_screen")

        # Instructions
        self._canvas.create_text(GUI.CANVAS_WIDTH/2,
                                 GUI.CANVAS_HEIGHT/2 +
                                 (GUI.PADDING * 2),
                                 fill="white", font="System 15 ",
                                 text="press 'space' to make the bird flap",
                                 anchor="center", tags="start_screen")

        self._window.mainloop()

    def _start_game(self):
        """
        Start game.

        Remove objects from the start screen
        then runs main loop

        """
        # Remove play button
        self._play_button.place_forget()
        # Remove Start screen
        self._canvas.delete("start_screen")
        # Set bird y vel to 0
        self._bird.y_vel = 0
        # Running the main loop function
        self._game_loop()

    def _flap(self, _):
        """
        Set y velocity of bird to jump_height.

        :param:
            _: this parameter is needed but not used
        """
        self._bird.y_vel = self._FLAP_HEIGHT

    def _game_loop(self):
        """
        Loop through game.

        moves bird and paddle
        checks if pipe is outside the canvas
        checks collision
        if bird collides with pipe end the game
        updates score if bird has passed a pipe
        """
        # Move bird
        self._bird.move_bird()

        # Move pipe
        self._pipe.move_pipe()

        # Checks if pipe is outside canvas
        pipe_end = self._pipe.pipe_end()

        # If pipe outside canvas create new pipe
        if pipe_end:
            self._pipe = Pipe(self._canvas)

        # The x positions of the bird and the pipe
        pipe_x = self._pipe.get_pipe_x()
        bird_x = self._bird.get_bird_x()

        # If the bird has passed the pipe add 1 to the score
        if bird_x > pipe_x and not self._pipe.has_scored:
            self._score += 1
            self._pipe.has_scored = True
        # Updating score label
        self._canvas.itemconfig(self._score_text, text=self._score)

        # Loops method
        loop = self._window.after(GUI._REFRESH_RATE, lambda: self._game_loop())

        # Checks if bird is colliding with pipe
        collision = self._bird.check_collision()
        if collision:
            # If the bird collides with the pipe end game
            # show game over screen
            self._window.after_cancel(loop)
            self._game_end()

    def _game_end(self):
        """
        End Game.

        allows the user to play again or exit the program
        updates high score
        """
        button_width = 50

        # Disable 'space'
        self._window.unbind_class("Button", "<Key-space>")

        # Game over text
        self._canvas.create_text(GUI.CANVAS_WIDTH / 2,
                                 GUI.CANVAS_HEIGHT / 2 -
                                 (GUI.PADDING * 2),
                                 fill="white", font="System 40 bold",
                                 text="Game Over", tags="game_over_text")

        # Places Try again and Exit buttons
        self._reset_button.place(x=(self.CANVAS_WIDTH/2) - button_width,
                                 y=self.CANVAS_HEIGHT/2)
        self._exit_button.place(x=self.CANVAS_WIDTH/2 - button_width,
                                y=self.CANVAS_HEIGHT/2 + self.PADDING)

        # Update high score if current score is greater than high score
        if self._score > self._hs:
            self._hs = self._score

        # Place high score text
        self._canvas.create_text(GUI.CANVAS_WIDTH -
                                 GUI._TEXT_PADDING,
                                 GUI._TEXT_PADDING,
                                 fill="white", font="System 20 bold",
                                 text=f"High score : {self._hs}", anchor="ne",
                                 tags="game_over_text")

    def _reset_game(self):
        """
        Reset Game.

        reset the bird to starting position
        reset the pipe and delete the current pipe off the canvas
        remove the exit and play again buttons
        reset the score
        run the game loop again
        """
        # Reset bird
        self._bird.reset_bird()

        # Delete pipe of canvas
        self._pipe.destroy_pipe()

        # Reset pipe
        self._pipe = Pipe(self._canvas)

        # Remove game over text
        self._canvas.delete("game_over_text")

        # Remove end buttons from screen
        self._reset_button.place_forget()
        self._exit_button.place_forget()

        # Reset score
        self._score = 0

        # Continue game loop
        self._game_loop()


class Bird:
    """
    A class that creates a bird.

    creates bird on the canvas that the player can control
    the bird has gravity and can flap

    Attributes
    ----------
    y_vel : int
        The vertical velocity of the bird
    _canvas : tkinter canvas
        The canvas where the bird is created
    _bird : canvas object
        A rectangle on the canvas that the player controls

    """

    _BIRD_WIDTH = 50
    _GRAVITY = 1

    def __init__(self, canvas):
        """
        Construct bird.

        Constructs a bird that is affected by gravity
        and can be moved by the player
        :param canvas: The canvas is where the bird will be created
        """
        self.y_vel = 0
        self._canvas = canvas

        # Creates bird
        self._bird = self._canvas.create_rectangle(GUI.PADDING,
                                                   GUI.CANVAS_HEIGHT / 2 -
                                                   self._BIRD_WIDTH / 2,
                                                   GUI.PADDING +
                                                   self._BIRD_WIDTH,
                                                   GUI.CANVAS_HEIGHT / 2 +
                                                   self._BIRD_WIDTH / 2,
                                                   fill="#f1f72d")

    def move_bird(self):
        """
        Move bird.

        adds certain amount to y velocity to act as gravity
        """
        # Adds gravity variable to y velocity
        self.y_vel += self._GRAVITY

        # Checking if bird moves out of bounds
        # Checks if bottom left corner is below canvas after it moves
        if self._canvas.coords(self._bird)[3] + self.y_vel >= \
                GUI.CANVAS_HEIGHT:
            # Sets y velocity to the gap between the bird and the floor
            self.y_vel = GUI.CANVAS_HEIGHT - \
                          self._canvas.coords(self._bird)[3]

        # Checks if top right corner is above the canvas after it moves
        elif self._canvas.coords(self._bird)[1] + self.y_vel <= 0:
            # Sets y velocity to the gap between the bird and the top
            self.y_vel = 0 - self._canvas.coords(self._bird)[1]

        # Moves bird by y velocity
        self._canvas.move(self._bird, 0, self.y_vel)

    def get_bird_x(self):
        """
        Get bird x coordinate of top left corner.

        This value will be used in checking if the bird has passed the pipe
        :return:
        """
        return self._canvas.coords(self._bird)[0]

    def check_collision(self):
        """
        Check collision of bird.

        :return:If anything is overlapping with the bird return true
        also if bird is at the bottom of the screen return true
        else return false
        """
        # c is coordinates of bird
        c = self._canvas.coords(self._bird)
        # Check if there is anything overlapping
        overlap = self._canvas.find_overlapping(c[0], c[1], c[2], c[3])
        # If overlap return true
        if len(overlap) > 1:
            return True
        # If the bird is at the bottom of the screen return true
        elif self._canvas.coords(self._bird)[3] >= GUI.CANVAS_HEIGHT:
            return True
        else:
            return False

    def reset_bird(self):
        """Reset Bird."""
        # Reset bird back to middle of the screen
        self._canvas.moveto(self._bird, GUI.PADDING, GUI.CANVAS_HEIGHT / 2 -
                            self._BIRD_WIDTH / 2)
        # Set y vel to 0
        self.y_vel = 0


class Pipe:
    """
    A class that creates a pipe that moves across the screen.

    creates pipe off canvas that moves left along the screen that the bird has
    to fly through

    Attributes
    ----------
    _canvas : tk canvas
        A canvas that the pipe gets drawn on
    _top_pipe : canvas object
        Top half of the pipe that has a random height
    _bottom_pipe : canvas object
        The bottom half of the pipe based off the top half
    has_scored : bool
        A bool that stores whether the bird has passed the pipe
    """

    _PIPE_WIDTH = 50
    _PIPE_GAP = 175
    _MOVE_SPEED = -7
    _MIN_PIPE_HEIGHT = 50
    _MAX_PIPE_HEIGHT = int((GUI.CANVAS_HEIGHT / 2) + 100)

    def __init__(self, canvas):
        """
        Construct necessary attributes for the pipe.

        also lowers the pipe on the canvas
        :param canvas: The canvas is where the pipe will be created
        """
        self._canvas = canvas

        top_pipe_height = randint(self._MIN_PIPE_HEIGHT, self._MAX_PIPE_HEIGHT)

        # Creates top half of pipe
        self._top_pipe = self._canvas.create_rectangle(GUI.CANVAS_WIDTH,
                                                       0, GUI.CANVAS_WIDTH
                                                       + self._PIPE_WIDTH,
                                                       top_pipe_height,
                                                       fill="#1ac943",
                                                       tags="Pipe")
        # Creates bottom half of pipe
        self._bottom_pipe = self._canvas.create_rectangle(GUI.CANVAS_WIDTH,
                                                          top_pipe_height +
                                                          self._PIPE_GAP,
                                                          GUI.CANVAS_WIDTH +
                                                          self._PIPE_WIDTH,
                                                          GUI.CANVAS_HEIGHT,
                                                          fill="#1ac943",
                                                          tags="Pipe")
        # Pipe can only add score once
        # after it has added score this gets set to True
        self.has_scored = False

        # Lowers the pipe so that the text is displayed on top of it
        self._canvas.lower("Pipe")

    def move_pipe(self):
        """Move pipe."""
        # Move pipe by the pipe speed
        self._canvas.move("Pipe", self._MOVE_SPEED, 0)

    def get_pipe_x(self):
        """
        Get the x value of the bottom right corner of the top pipe.

        This value will be used to check if the Bird has passed the pipe
        :return: The coordinates of the x value of the bottom right corner
        """
        return self._canvas.coords(self._top_pipe)[2]

    def pipe_end(self):
        """
        Check if pipe has reached the end.

        :return: True if at end or False if not at end
        """
        if self._canvas.coords(self._top_pipe)[2] < 0:
            self.destroy_pipe()
            return True
        else:
            return False

    def destroy_pipe(self):
        """Delete pipe off canvas."""
        self._canvas.delete("Pipe")


if __name__ == "__main__":
    GUI()
