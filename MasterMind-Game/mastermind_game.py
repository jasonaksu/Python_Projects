import turtle
import random
import datetime
import os


class MastermindGame:
    """
    This class illustrates a Mastermind game, implementing the classic
    code-breaking board game  in a graphical user interface using Python's
    turtle module. the game allows user to guess the "secret code" a set of
    four colors chosen out of six possible colors. Guesses with correct
    positions called "bulls" and represented by black pegs.Correct
    guesses with incorrect positions called "cows" and represented
    by red pegs. The class manages the game's state user interactions,
    draws game elements and maintains leaderboard by creating leaderboard.txt
    to track scores.
    """
    def __init__(self, test_mode=False):
        """
        Creates a new instance for the game. Sets up the game configuration,
        including colors, radius for pegs, number of guesses, secret code, vs.
        If not in test mode it cals the game graphics. If in test mode
        starts without graphics.
        :param test_mode: Boolean flag indicates whether the game is being
        initialized in test mode or not. The default is False.
        """
        # Game Configuration
        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]
        self.radius = 15
        self.num_guesses = 10
        self.guess_spots = 4
        self.secret_code = random.sample(self.colors, 4)
        self.guess_history = []
        self.current_guess = []
        self.button_locations = {}
        self.leaderboard_file = "leaderboard.txt"
        self.error_log_file = "mastermind_errors.err"
        if not test_mode:
            self.game_graphics()

    def game_graphics(self):
        """
        Sets up the graphical UI for the Mastermind game.Includes
        screen configuration, drawing and texting turtles, adding shapes for
        gif buttons, and initializing UI elements such as arrow indicator,
        pop-ups and event bindings.
        """
        # Screen Configuration
        self.screen = turtle.Screen()
        self.screen.title("CS 5001 Mastermind Code Game")
        self.screen.setup(width=500, height=600)
        self.screen.tracer(0)

        # Turtle For Drawing
        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        self.drawer.hideturtle()
        self.drawer.penup()

        # Turtle for Text
        self.text_drawer = turtle.Turtle()
        self.text_drawer.hideturtle()
        self.text_drawer.penup()

        # Turtle for Gif Images
        self.screen.addshape("checkbutton.gif")
        self.screen.addshape("xbutton.gif")
        self.screen.addshape("quit.gif")
        self.screen.addshape("file_error.gif")
        self.screen.addshape("Lose.gif")
        self.screen.addshape("quitmsg.gif")
        self.screen.addshape("winner.gif")

        # Button x and y ranges
        self.button_locate = {
            "check": {"x_range": (40, 80), "y_range": (-230, -190)},
            "reset": {"x_range": (80, 120), "y_range": (-230, -190)},
            "quit": {"x_range": (135, 205), "y_range": (-230, -190)}
        }

        self.initialize_arrow_indicator()
        self.popup_turtle = None

        # Binding Click Clicking
        self.screen.onclick(self.on_screen_click, 1)

        # Start The Game
        self.start_game()

    # ***** ~ Drawing Methods ~ *****
    def circle(self, x, y, radius, color):
        """
        Draws a circle with a given radius and color at a selected location.
        :param x: The x position of the circle's center.
        :param y: The y position of the circles center.
        :param radius: The radius of the circle.
        :param color: Color of the circle.
        """
        self.drawer.penup()
        self.drawer.goto(x, y - radius)
        self.drawer.fillcolor(color)
        self.drawer.pendown()
        self.drawer.begin_fill()
        self.drawer.circle(radius)
        self.drawer.end_fill()
        self.drawer.penup()

    def rectangle(self, x, y, width, height, color):
        """
        Draws a rectangle at a given location with specified
        dimensions and color.
        :param x: The x position of the rectangle's top left corner.
        :param y: The y  position of the rectangle's top left corner.
        :param width: Width of the rectangle.
        :param height: Height of the rectangle.
        :param color: Color of the rectangle.
        """
        self.drawer.pensize(3)
        self.drawer.penup()
        self.drawer.goto(x, y)
        self.drawer.fillcolor(color)
        self.drawer.pendown()
        self.drawer.begin_fill()
        for _ in range(2):
            self.drawer.forward(width)
            self.drawer.right(90)
            self.drawer.forward(height)
            self.drawer.right(90)
        self.drawer.end_fill()
        self.drawer.penup()
        self.drawer.pensize(1)

    def guessing_frame(self):
        """Draws the guessing frame of the game"""
        start_x = -180
        start_y = 250
        # draw the outer rectangle of the guesing frame
        self.rectangle(-230, 280, 270, 420, "white")
        self.drawer.goto(-150, 250)
        self.drawer.color("black")

        # Loop to create rows in the guessing frame
        for i in range(10):

            # Nested loop to create individual guessing spots.
            for j in range(4):
                # Determine positions.
                x_position = start_x + j * 40
                y_position = start_y - i * 40
                # Draw the circle
                self.circle(x_position, y_position, self.radius, "white")

            # Nested loop to create scoring indications
            for k in range(2):
                # Determine positions.
                x_position = start_x + 160 + k * 15
                y_position = start_y - i * 40 + 10

                # Draw the circle
                self.circle(x_position, y_position, 5, "lightgrey")

            for k in range(2):
                # Determine positions.
                x_position = start_x + 160 + k * 15
                y_position = start_y - i * 40 - 5

                # Draw the circle.
                self.circle(x_position, y_position, 5, "lightgrey")

    def scoring_pegs(self, bulls, cows, row):
        """
        Draws scoring pegs to display correct and incorrect guesses
        (bulls, and cows).
        :param bulls:The number of pegs for correct color and position (black)
        :param cows: The number of pegs for correct color but
        wrong positions. (red)
        :param row: The row number on the grid where the pegs are to be drawn.
        """
        new_start_x = -180 + (self.guess_spots * 40)
        start_y = 250 - (row * 40)

        # loop for draw up to four scoring pegs
        for i in range(4):
            # Determine the color.
            if i < bulls:
                color = "black"  # Bull: Correct color and position.
            elif i < bulls + cows:
                color = "red"  # Cow: Correct color wrong position.
            else:
                color = "lightgrey"  # Blank circle for wrong guesses.

            # Calculates a vertical offset for the pegs
            y_offset = 10 if i < 2 else -5

            # Draw the circle for scoring pegs.
            self.circle(new_start_x + (i % 2) * 15, start_y + y_offset, 5, color)

    # ***** ~ Methods for Creating Buttons ~ *****
    def color_buttons(self):
        """
        Draws color selection buttons on the designated area
        of the game screen. Iterates through the available colors, creating
        and positioning a button for each color. Updates button_locations
        with the coordinates of each color button.
        """
        start_x = -180
        start_y = -210

        # Draw rectangle border for action buttons.
        self.rectangle(220, -245, -450, -70, "white")
        self.drawer.goto(-150, 250)
        self.drawer.color("black")

        # iterates self.color for different colors
        for i, color in enumerate(self.colors):
            # i * 35 placing buttons 35 units apart each other
            x = start_x + i * 35
            # Updates button dictionary to identify which button clicked.
            self.button_locations[color] = x, start_y
            # Selected color turns white
            button_color = "white" if color in self.current_guess else color
            self.circle(x, start_y, self.radius, button_color)

    def gif_buttons(self):
        """
        Creates and positions gif buttons (check, reset,  quit) on the game.
        Initializes individual turtle instances for each button, and places
        them at given spots. Also updates the button_locations attribute
        for click detection.
        """
        # Starting positions for gif buttons.
        start_x = 60  # Position after the last color button
        start_y = -210 # y position of the gif buttons

        # Check Button
        check_button_turtle = turtle.Turtle()
        check_button_turtle.shape("checkbutton.gif")
        check_button_turtle.penup()
        check_button_turtle.goto(start_x, start_y)
        check_button_turtle.stamp()

        # Reset Button
        start_x += 40  # Position from the Check Button
        reset_button_turtle = turtle.Turtle()
        reset_button_turtle.shape("xbutton.gif")
        reset_button_turtle.penup()
        reset_button_turtle.goto(start_x, start_y)
        reset_button_turtle.stamp()

        # Quit Button
        start_x += 70  # Position from the Reset Button
        quit_button_turtle = turtle.Turtle()
        quit_button_turtle.shape("quit.gif")
        quit_button_turtle.penup()
        quit_button_turtle.goto(start_x, start_y)
        quit_button_turtle.stamp()

        # Button locations for click detection
        self.button_locations['check'] = (start_x - 60, start_y)
        self.button_locations['reset'] = (start_x, start_y)
        self.button_locations['quit'] = (start_x + 70, start_y)

    # ***** ~ Pop-up Methods, Showing Message and Log Errors ~ *****
    def show_popup(self, gif_filename, display_time=5000):
        """
        Shows a popup with the selected GIF file for a given time.
        :param gif_filename: The name of the GIF file to display.
        :param display_time: The duration of the popup in milliseconds.
        """
        if self.popup_turtle is None:
            self.popup_turtle = turtle.Turtle()
            self.popup_turtle.hideturtle()
            self.popup_turtle.penup()

        self.screen.addshape(gif_filename)
        self.popup_turtle.shape(gif_filename)
        self.popup_turtle.goto(0, 0)  # Center of the screen

        # Stamps the popup image onto the screen
        popup_stamp = self.popup_turtle.stamp()
        # Refresh the screen to ensure gif is displayed.
        self.screen.update()

        # Nested function for clearing the popup
        def hide_popup():
            # Remove the Gif image from the screen
            self.popup_turtle.clearstamp(popup_stamp)
            self.popup_turtle.hideturtle()

        self.screen.ontimer(hide_popup, display_time)

    def get_name(self):
        """Prompts the player to enter their name and store it"""
        # Prevents overwriting an existing player name
        # Ensure the name requested only when necessary
        if not hasattr(self, 'player_name') or not self.player_name:
            message = "Your name:"
            self.player_name = self.screen.textinput("CS 5001 Mastermind Code Game", message)

    def display_secret_code(self, secret_code):
        """
        Displays the secret code at the end of the game and prompts the player
        for a new game. If player clicks to the ok button starts the new game.
        If player click to the cancel button quit the game and show quit popup
        :param secret_code: The secret code shown to the player.
        """
        # Convert secret code to string
        secret_code_str = ' '.join(secret_code)
        # Display the secret code and ask for the new game.
        response = self.screen.textinput(
            "Game Over",
            f"The secret code was: {secret_code_str}\n"
            f"Your score: {self.calculate_score()}\n"
            "Click OK to play again or Cancel to exit"
        )
        # Handle players response quit or start the new game.
        if response is None:
            self.show_popup("quitmsg.gif", 3000)
            self.screen.ontimer(self.quit_game, 3000)
        else:
            self.start_new_game()

    def log_error(self, error_message):
        """
        Logs error messages with a timestamp
        :param error_message: Error message to be logged.
        """
        # Generate time stamp in the format
        # Year, Month, Day, Hour, Minute ad Second
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.error_log_file, "a") as file:  # Open error log file.
            # Write error message
            file.write(f"{timestamp} - {error_message}\n")

    def show_message(self, gif_filename):
        """
        Message popup using a GIF image
        :param gif_filename: The gif to be used for the popup message.
        """
        # Add GIF image as a shape
        self.screen.addshape(gif_filename)

        message_turtle = turtle.Turtle()
        message_turtle.hideturtle()
        message_turtle.penup()
        # Setting the Turtle shape to the gif image.
        message_turtle.shape(gif_filename)
        message_turtle.goto(0, 0)  # Center of the screen
        message_turtle.stamp()  # Display the gif image

        # Gif image displays for 5 second then clear
        self.screen.ontimer(lambda: message_turtle.clear(), 5000)

    # ***** ~ Leaderboard Logic ~ *****
    def draw_leaderboard(self):
        """
        Draws the leaderboard frame on the game board
        with a title "Leaders".
        """
        self.drawer.color("blue")  # Blue border for the leaderboard.
        # Drawing the leaderboard frame with specified position and dimension.
        self.rectangle(50, 280, 170, 420, "white")
        self.drawer.goto(100, 250)
        # Write the title leader
        self.drawer.write("Leaders:", font=("Times", 18, "bold"))
        self.drawer.color("black")  # Turn turtle pen color to black.

    def write_leaderboard(self, leaderboard):
        """
        Writes the leaderboard to a txt file
        :param leaderboard: Alist of tuples including players name and score.
        """
        with open(self.leaderboard_file, "w") as file:
            for name, score in leaderboard:
                file.write(f"{name}: {score}\n")

    def read_leaderboard(self):
        """
        Reads the leaderboard from Leaderboard.txt file,
        and displays the top 10 score
        """
        try:
            with open(self.leaderboard_file, "r") as file:
                # Initialize the empty list to store the entries.
                leaderboard = []
                for line in file:
                    parts = line.strip().split(': ')
                    # Check if the line correctly break into to line.
                    if len(parts) == 2:  # For name and score
                        name, score_str = parts
                        score = int(score_str)  # Convert score str to int.
                        #  Add the tuple of name and score to the leaderboard.
                        leaderboard.append((name, score))
                leaderboard.sort(key=lambda x: x[1])  # Ascending order.
                return leaderboard[:10]  # Return top 10 scores.
        except FileNotFoundError:
            self.log_error("leaderboard file not found.")
            return []
        except Exception as e:
            self.log_error(f"Error reading leaderboard file: {e}")
            return []

    def leaderboard_updated_score(self, score, player_name):
        """
        Updates the leaderboard with a score for a specific player name.
        Responsible for updating existing players score and adding new
        players to leaderboard to keep leader board up-to-date.
        :param score: Score to update for the player
        :param player_name: The name of the player
        """
        # Read current leaderboard
        leaderboard = self.read_leaderboard()

        # Update the players score.
        # check if the current players name matches the provided name.
        for i, entry in enumerate(leaderboard):
            if entry[0] == player_name:
                leaderboard[i] = (player_name, score)
                break
        else:
            leaderboard.append((player_name, score))

        # Sort in ascending order.
        leaderboard.sort(key=lambda x: x[1])
        leaderboard = leaderboard[:10]  # Ensure top 10 score in the leaderboard
        self.write_leaderboard(leaderboard)

    def display_leaderboard(self):
        """
        Displays the leaderboard on the designated area of the screen,
        showing players name and score.
        """
        leaderboard_start_x = 70
        leaderboard_start_y = 230
        leaderboard = self.read_leaderboard()
        self.text_drawer.clear()

        # Display name and score.
        for index, (name, score) in enumerate(leaderboard):
            y_coordinate = leaderboard_start_y - index * 20
            self.text_drawer.goto(leaderboard_start_x, y_coordinate)

            leaderboard_text = f"{index + 1}. {name}: {score}"
            font_settings = ("Arial", 14, "normal")

            self.text_drawer.write(leaderboard_text, align="left", font=font_settings)

    def leaderboard_with_player(self):
        """
        Initializes the leaderboard with the attending player adds them
        to the leaderboard file if not already written.
        """
        #  Read the current leaderboard.
        leaderboard = self.read_leaderboard()

        #  Check if the player is already in the leaderboard.
        if not any(entry[0] == self.player_name for entry in leaderboard):
            #  add the player with a base score of 0
            leaderboard.append((self.player_name, 0))

        # Sort the leaderboard in ascending order (smallest first)
        leaderboard.sort(key=lambda x: x[1])
        leaderboard = leaderboard[:10]

        #  Update the leaderboard file.
        self.write_leaderboard(leaderboard)
        self.display_leaderboard()

    def calculate_score(self):
        """ Calculate the score for the number of guesses made."""
        score = len(self.guess_history)
        return score

    # ***** ~ Methods for Guess Logic ~ *****
    def initialize_arrow_indicator(self):
        """
        Initializes an arrow indicator to show the current guess row.
        """
        self.arrow_indicator = turtle.Turtle()
        self.arrow_indicator.shape('arrow')
        self.arrow_indicator.color('red')
        self.arrow_indicator.pencolor('black')
        self.arrow_indicator.penup()

    def draw_arrow_indicator(self, row):
        """
        Places the arrow indicator at the selected row.
        :param row: The row number arrow indicator should be placed.
        """
        y_position = 250 - row * 40
        self.arrow_indicator.goto(-220, y_position)

    def display_guess_history(self):
        """
        Displays the history of guesses along with their evaluations.
        Each past guess, and its bulls and cows are drawn on the game board.
        """
        start_x = -180
        for i, (guess, bulls, cows) in enumerate(self.guess_history):
            start_y = 250 - (i * 40)
            # Nested loop iterate over each color in current guess
            for j, color in enumerate(guess):
                self.circle(start_x + j * 40, start_y, 15, color)

            # Call scoring pegs method to display bulls and cows
            # i parameter is used to position the scoring correctly.
            self.scoring_pegs(bulls, cows, i)

    def draw_current_guess(self):
        """
        Marks the players current guess to the game board. Visualizes each
        color in the current guess as a circle at a specific place.
        """
        start_x = -180
        start_y = 250 - (len(self.guess_history) * 40)
        for i, color in enumerate(self.current_guess):
            self.circle(start_x + i * 40, start_y, 15, color)

    def check_guess(self, guess):
        """
        This method evaluate the guess against secret code.
        :param guess: List for the users guess
        :return: Tuple containing number of bulls and cows.
        """
        bulls = 0
        cows = 0
        secret_code_copy = self.secret_code[:]

        # Count the bulls
        for i in range(len(guess)):
            if guess[i] == self.secret_code[i]:
                bulls += 1
                # None to avoid recounting it as a cow
                secret_code_copy[i] = None

        # Count the cows
        for i in range(len(guess)):
            if guess[i] != self.secret_code[i] and guess[i] in secret_code_copy:
                cows += 1
                secret_code_copy.remove(guess[i])

        return bulls, cows

    def confirm_guess(self):
        """
        Confirms the current guess, assesses it, and updates the game.
        Calculates the bulls and cows, updates the guess history,
        redraws the gameboard, and reviews for the end of the game.
        """
        if len(self.current_guess) != self.guess_spots:
            print("Not enough colors selected.")
            return

        # Calculate bulls and cows.
        bulls, cows = self.check_guess(self.current_guess)

        # Update guess history and scoring pegs.
        self.guess_history.append((self.current_guess, bulls, cows))
        self.scoring_pegs(bulls, cows, len(self.guess_history) - 1)

        # Move the arrow only if the number of guesses less than 10.
        if len(self.guess_history) < self.num_guesses:
            self.draw_arrow_indicator(len(self.guess_history))

        self.current_guess = []
        self.update_game_board()

        # Check if the game is over.
        if bulls == self.guess_spots:
            # Secret code found.
            self.show_popup("winner.gif", 5000)
            player_score = self.calculate_score()
            self.leaderboard_updated_score(player_score, self.player_name)
            self.display_leaderboard()
            self.display_secret_code(self.secret_code)
        elif len(self.guess_history) == self.num_guesses:
            # Could not find the secret code.
            self.show_popup("Lose.gif", 5000)
            player_score = self.calculate_score()
            self.leaderboard_updated_score(player_score, self.player_name)
            self.display_leaderboard()
            self.display_secret_code(self.secret_code)

    def reset_guess(self, x, y):
        """
        Reset the current guess based on user interaction.
        :param x: x position of the click.
        :param y: y position of the click
        """
        if 80 <= x <= 120 and -230 <= y <= -190:
            self.current_guess = []
            self.update_game_board()

# ***** ~ Click Events ~ *****
    def click_in_button(self, x, y, button):
        """
        Check if the click in the button area.
        :param x: x position of the click
        :param y: y position of the click
        :param button: A dictionary with x and y range keys representing
        the buttons location
        :return: bool: True if the click in button. False otherwise.
        """
        return (
            button["x_range"][0] <= x <= button["x_range"][1] and
            button["y_range"][0] <= y <= button["y_range"][1]
        )

    def click_in_circle(self, x, y, center_x, center_y, radius):
        """
        Checks if the click in the circle area.
        :param x: x position of the click.
        :param y: y position of the click.
        :param center_x: x position of the circles center.
        :param center_y: y position of the circles center.
        :param radius: Radius of the circle.
        :return: bool: True if the click in circle. False otherwise.
        """
        return(x - center_x)**2 + (y - center_y)**2 <= radius**2

    def color_click(self, x, y):
        """
        Process the click for a color button. Adds the selected color to the
        current guess if the maximum number of colors has not been selected.
        :param x: x position of the click
        :param y: y position of the click
        """
        for color, (bx, by) in self.button_locations.items():
            if self.click_in_circle(x, y, bx, by, self.radius):
                if len(self.current_guess) >= self.guess_spots:
                    print("Maximum of 4 colors selected")
                    return
                if color not in self.current_guess:
                    self.current_guess.append(color)
                    self.circle(bx, by, self.radius, "white")
                    self.update_game_board()

    def quit_button_click(self):
        """
        Executes the quit button click. Displays the quitmsg.gif popup
        """
        self.show_popup("quitmsg.gif", 3000)
        self.screen.ontimer(self.quit_game, 3000)

    def on_screen_click(self, x, y):
        """
        Determine which button was clicked and calls the related method.
        :param x: x position of the click
        :param y: y position of the click
        """
        if self.click_in_button(x, y, self.button_locate["check"]):
            self.confirm_guess()
        elif self.click_in_button(x, y, self.button_locate["reset"]):
            self.reset_guess(x, y)
        elif self.click_in_button(x, y, self.button_locate["quit"]):
            self.quit_button_click()
        else:
            self.color_click(x, y)

    # ***** ~ Game Start, Setup, Update Methods ~ *****
    def update_game_board(self):
        """
        Refreshes and redraws the entire game board. Clears any popups and
        redraws all game components, including the guessing frame,
        color buttons, action buttons, current guess, guess history,
        and the leaderboard
        """
        # Clear popups
        if self.popup_turtle is not None:
            self.popup_turtle.clearstamps()
            self.popup_turtle.hideturtle()

        # Redraw the game board.
        self.drawer.clear()
        self.guessing_frame()
        self.color_buttons()
        self.gif_buttons()
        self.draw_current_guess()
        self.display_guess_history()
        self.draw_leaderboard()
        self.display_leaderboard()
        self.screen.update()

    def initialize_game_board(self):
        """Initialize the main components of the game board"""
        self.get_name()
        self.leaderboard_with_player()
        self.display_leaderboard()
        self.draw_arrow_indicator(0)
        self.update_game_board()

    def start_game(self):
        """
        Checks for the existence of the leaderboard file, displays an error
        popup if the file is missing, and initializes the game board.
        Also, ensures that the arrow indicator is hidden initially and shown
        only when the game setup is complete.
        """
        # Check if the leaderboard file exists show a popup if not found.
        if not os.path.exists(self.leaderboard_file):
            self.arrow_indicator.hideturtle()
            self.show_popup("leaderboard_error.gif", 3000)

            def continue_game_setup():
                """Continue setup the game after the error popup"""
                self.initialize_game_board()
                self.arrow_indicator.showturtle()
                self.screen.update()

            # Schedule the game setup after error popup.
            self.screen.ontimer(continue_game_setup, 1000)
        else:
            # If leaderboard file exist start the game
            self.initialize_game_board()
            self.arrow_indicator.showturtle()
            self.screen.update()

        self.screen.mainloop()

    def start_new_game(self):
        """
        Resets the game and starts a new game. Clears the game board, prompts
        for the player's name initializes the leaderboard, and redraws
        the game board for a new game session
        """
        if self.popup_turtle is not None:
            self.popup_turtle.clearstamps()
            self.popup_turtle.hideturtle()

        # Reset the game
        self.current_guess = []
        self.guess_history = []
        self.secret_code = random.sample(self.colors, self.guess_spots)

        # Prompt for the player name
        self.player_name = None
        self.get_name()

        # Initialize the leaderboard with the new player.
        self.leaderboard_with_player()

        # Draw the game board.
        self.update_game_board()

    def reset_game(self):
        """
        Resets the current game to start a new round. Clears the current
        guess and guess history, generates a new secret code,
        and updates the game board.
        """
        if self.popup_turtle is not None:
            self.popup_turtle.clearstamps()
            self.popup_turtle.hideturtle()

        self.current_guess = []
        self.guess_history = []
        self.secret_code = random.sample(self.colors, self.guess_spots)
        self.update_game_board()

    def quit_game(self):
        """
        Quit game and closes the game window.
        """
        self.screen.bye()


# Main function to start the game.
def main():
    game = MastermindGame()


if __name__ == "__main__":
    main()
