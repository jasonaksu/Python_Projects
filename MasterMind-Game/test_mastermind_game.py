import unittest
from mastermind_game import MastermindGame


class TestMastermindGame(unittest.TestCase):
    """
    This test class possesses unit test for the Mastermind game class.
    It tests the game's guess logic by assessing different scenarios
    to confirm that it correctly computes the number of bulls and cows.
    """
    def setUp(self):
        """
        Before each test scenarios, this method is called to initialize
        the Mastermind game in test mode (no graphical interface) and sets
        a preselected secret code for accurate testing.
        """
        # Prepare the game for test mode without graphics.
        self.game = MastermindGame(test_mode=True)
        # Create the defined secret code for accurate testing.
        self.game.secret_code = ["black", "red", "purple", "blue"]

    def test_scenarios(self):
        """
        This method tests the game's guess logic of various scenarios against
        a predefined secret code.
        """
        # Specify test cases as a tuple holding the user guess and expected
        # number of bulls and cows.

        test_cases = [
            # Two colors at correct place and two wrong colors.
            (["black", "red", "yellow", "green"], 2, 0),
            # 2 color in the correct and, 2 colors in the wrong place.
            (["purple", "red", "black", "blue"], 2, 2,),
            # All colors are correct but in the wrong spot.
            (["purple", "black", "blue", "red"], 0, 4),
            # All colors are correct and in the correct place.
            (["black", "red", "purple", "blue"], 4, 0)
        ]

        # Loop over the test cases.
        for user_guess, expected_bulls, expected_cows in test_cases:
            # Check the use guess and get the number of bulls and cows.
            bulls, cows = self.game.check_guess(user_guess)
            # Claim that the computed bulls and cows match the expected value.
            self.assertEqual(bulls, expected_bulls)
            self.assertEqual(cows, expected_cows)


if __name__ == '__main__':
    unittest.main()
