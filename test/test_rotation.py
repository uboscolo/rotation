import io
import unittest
from contextlib import redirect_stdout

from rotation import Player, load_positions, rotate


class TestRotationModule(unittest.TestCase):
    def test_load_positions_contains_expected_player(self):
        positions = load_positions()
        self.assertIn("Piero", positions)
        self.assertEqual(positions["Piero"]["defense"]["favorite"], "RB")

    def test_rotate_with_three_players_returns_same_players(self):
        players = ["A", "B", "C"]
        self.assertEqual(rotate(1, players), players)

    def test_rotate_with_four_players_period_two(self):
        players = ["A", "B", "C", "D"]
        self.assertEqual(rotate(2, players), ["A", "B", "D"])

    def test_rotate_too_few_players_prints_error_and_returns_empty(self):
        out = io.StringIO()
        with redirect_stdout(out):
            result = rotate(1, ["A", "B"])
        self.assertEqual(result, [])
        self.assertIn("Error, not enough players: 2", out.getvalue())

    def test_player_rejects_invalid_position(self):
        player = Player("Test")
        with self.assertRaises(TypeError):
            player.position = "INVALID"


if __name__ == "__main__":
    unittest.main()
