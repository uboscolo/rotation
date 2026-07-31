import json
import os
import tempfile
import unittest

from rotation import Player, Unit, Team, load_positions


class TestLoadPositions(unittest.TestCase):
    def test_contains_expected_player(self):
        positions = load_positions("database/B4_lions.json")
        self.assertIn("Piero", positions)
        self.assertEqual(positions["Piero"]["defense"]["favorite"], "RB")

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_positions("database/nonexistent.json")


class TestPlayer(unittest.TestCase):
    def test_accepts_position_assignment(self):
        player = Player("Test")
        player.position = "INVALID"
        self.assertEqual(player.position, "INVALID")

    def test_name_setter_rejects_non_string(self):
        player = Player("Test")
        with self.assertRaises(TypeError):
            player.name = 123

    def test_name_setter_rejects_empty(self):
        player = Player("Test")
        with self.assertRaises(ValueError):
            player.name = ""


class TestUnit(unittest.TestCase):
    def test_invalid_name_raises(self):
        with self.assertRaises(ValueError):
            Unit("midfield", num_starters=3)

    def test_invalid_num_starters_raises(self):
        with self.assertRaises(ValueError):
            Unit("offense", num_starters=7)

    def test_valid_unit_creation(self):
        unit = Unit("defense", num_starters=3)
        self.assertEqual(unit.name, "defense")
        self.assertEqual(unit.num_starters, 3)


class TestTeamAddPlayer(unittest.TestCase):
    def _make_db(self, data: dict) -> str:
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(data, f)
        f.close()
        return f.name

    def setUp(self):
        self.db_missing_favorite = self._make_db(
            {"Alice": {"defense": {"alternate": "CB"}}}
        )
        self.db_missing_alternate = self._make_db(
            {"Alice": {"defense": {"favorite": "LB"}}}
        )
        self.db_valid = self._make_db(
            {"Alice": {"defense": {"favorite": "LB", "alternate": "CB"}}}
        )

    def tearDown(self):
        for path in [self.db_missing_favorite, self.db_missing_alternate, self.db_valid]:
            os.unlink(path)

    def test_missing_favorite_raises(self):
        team = Team("Test", 7, self.db_missing_favorite)
        with self.assertRaises(ValueError):
            team.add_player(Player("Alice"), "defense")

    def test_missing_alternate_raises(self):
        team = Team("Test", 7, self.db_missing_alternate)
        with self.assertRaises(ValueError):
            team.add_player(Player("Alice"), "defense")

    def test_player_not_in_db_raises(self):
        team = Team("Test", 7, self.db_valid)
        with self.assertRaises(ValueError):
            team.add_player(Player("Bob"), "defense")

    def test_player_not_in_unit_raises(self):
        team = Team("Test", 7, self.db_valid)
        with self.assertRaises(ValueError):
            team.add_player(Player("Alice"), "offense")


if __name__ == "__main__":
    unittest.main()
