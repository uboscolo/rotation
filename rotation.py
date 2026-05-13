"""
    This module provides utility functions for data processing.
    It includes functions for cleaning, transforming, and analyzing data.
"""
import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path

def load_positions() -> dict:
    """Loads player position preferences from database/players.json."""
    positions_file = Path(__file__).resolve().parent / "database" / "players.json"
    return json.loads(positions_file.read_text(encoding="utf-8"))

def rotate(period, players):
    """ rotate """
    indices_map = {4: {1: [1,2,3],
                       2: [1,2,4],
                       3: [1,3,4],
                       4: [2,3,4],
                       5: [1,2,3],
                       6: [1,2,4],
                       7: [1,3,4],
                       8: [2,3,4]}
                      }
    min_players = 3
    max_players = 6
    num_players = len(players)
    ret_players = []
    if num_players < min_players:
        print(f"Error, not enough players: {num_players}")
    elif num_players == min_players:
        ret_players = players
    elif num_players > max_players:
        print(f"Error, too many players: {num_players}")
    else:
        indices = indices_map[num_players][period]
        ret_players = [players[i-1] for i in indices]

    return ret_players


class Player:
    """
    Represents a player
    """

    def __init__(self, name: str):
        """
        Initializes a new Player object.

        Args:
            name (str): The player's name.
        """
        self.__name: str = name
        self.__starting_position = None
        self.__position = None

    @property
    def name(self) -> str:
        """The name of the player."""
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value:
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def position(self) -> str:
        """The position of the player."""
        return self.__position

    @position.setter
    def position(self, value: str):
        valid_positions = ["GK", "LB", "CB", "RB", "LW", "ST", "RW", "R"]
        if value not in valid_positions:
            raise TypeError(f"Position {value} not valid, needs to be one of {valid_positions}")
        self.__position = value

    @property
    def starting_position(self) -> str:
        """The starting position of the player."""
        return self.__starting_position

    @starting_position.setter
    def starting_position(self, value: str):
        valid_positions = ["GK", "LB", "CB", "RB", "LW", "ST", "RW", "R"]
        if value not in valid_positions:
            raise TypeError(f"Position {value} not valid, needs to be one of {valid_positions}")
        self.__starting_position = value


@dataclass
class UnitState:
    """Mutable state for a unit across periods."""
    starters: list = field(default_factory=list)
    reserves: list = field(default_factory=list)
    active_players: list = field(default_factory=list)
    inactive_players: list = field(default_factory=list)
    players_map: dict = field(default_factory=dict)
    assigned_positions: dict = field(default_factory=dict)

class Unit:
    """
    Represents a unit in a team, e.g. defense or offense
    """
    num_starters = 3
    rotate_map: dict = {4: {1: [1,2,3], 2: [1,2,4], 3: [1,3,4], 4: [2,3,4],
                            5: [1,2,3], 6: [1,2,4], 7: [1,3,4], 8: [2,3,4]},
                        5: {1: [1,2,3], 2: [1,4,5], 3: [2,3,4], 4: [1,2,5],
                            5: [3,4,5], 6: [1,2,4], 7: [1,3,5], 8: [2,4,5]},
                        6: {1: [1,2,3], 2: [4,5,6], 3: [2,3,4], 4: [1,5,6],
                            5: [3,4,5], 6: [1,2,6], 7: [1,3,5], 8: [2,4,6]}}

    def __init__(self, name: str, positions: list, positions_db: dict):
        """
        Initializes a new Unit object.

        Args:
            name (str): The unit's name.
            positions (list): The unit's positions, e.g. "LB", "CB", "RB".
        """
        self.__name: str = name
        if len(positions) != self.num_starters:
            raise ValueError(f"Unexpected number of positions {positions}.")
        self.__positions: list = positions
        self.__positions_db = positions_db
        self.__state = UnitState()

    @property
    def name(self) -> str:
        """The name of the unit."""
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value:
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def starters(self) -> list:
        """The unit's starters."""
        return self.__state.starters

    @property
    def reserves(self) -> list:
        """The unit's reserves."""
        return self.__state.reserves

    @property
    def active_players(self) -> list:
        """The unit's active players."""
        return self.__state.active_players

    @property
    def inactive_players(self) -> list:
        """The unit's inactive players."""
        return self.__state.inactive_players

    def get_player_by_name(self, name: str) -> Player:
        """
        Returns a player given their name

        Args:
            name (str): The player's name.
        """
        return self.__state.players_map.get(name)

    def __get_position_choices(self, player_name: str):
        """
        Returns the position choices after looking up in the DB

        Args:
            player_name (str): The player's name.
        """
        units = self.__positions_db.get(player_name)
        if not units:
            raise ValueError(f"No position units found for {player_name}.")
        choices = units.get(self.__name)
        if not choices:
            raise ValueError(f"No position choices found for {player_name}.")
        favorite = choices.get("favorite")
        alternate = choices.get("alternate")
        return (favorite, alternate)

    def __set_position(self, player_name: str):
        """
        Returns the position after looking up in the DB

        Args:
            player_name (str): The player's name.
        """
        favorite, alternate = self.__get_position_choices(player_name)
        if favorite not in self.__state.assigned_positions:
            position = favorite
        elif alternate not in self.__state.assigned_positions:
            position = alternate
        else:
            # Player not in a choice position
            for pos in self.__positions:
                if pos not in self.__state.assigned_positions:
                    position = pos
        self.__state.assigned_positions[position] = player_name
        return position

    def add_player(self, new_player: Player) -> None:
        """
        Adds a new player to the unit

        Args:
            new_player (Player): The player to add.
        """
        if new_player in self.__state.starters or new_player in self.__state.reserves:
            raise ValueError(f"Player {new_player.name} already in the {self.__name} unit.")

        current_starters = len(self.__state.starters)
        if current_starters == self.num_starters:
            # Reserves
            new_player.position = "R"
            new_player.starting_position = new_player.position
            self.reserves.append(new_player)
        else:
            new_player.position = self.__set_position(new_player.name)
            new_player.starting_position = new_player.position
            self.__state.starters.append(new_player)
        self.__state.players_map[new_player.name] = new_player
        # print(f"Adding {new_player.name} as {new_player.starting_position}")

    def swap(self, name: str, player: Player, **positions) -> None:
        """
        Swaps players

        Args:
            name (str): The player's name to swap out
            player (Player): The player to swap in
        """
        candidate = self.__state.players_map.get(name)
        default_starting_position = candidate.starting_position if candidate else None
        default_position = candidate.position if candidate else None
        starting_position = positions.get("starting_position", default_starting_position)
        position = positions.get("position", default_position)
        if not starting_position:
            raise ValueError("Starting position not defined.")
        if not position:
            raise ValueError("Active position not defined.")
        player.starting_position = starting_position
        player.position = position

        # Handle case of goalkeeper
        if starting_position == "R":
            self.__state.reserves[self.__state.reserves.index(candidate)] = player
        else:
            self.__state.starters[self.__state.starters.index(candidate)] = player
        if position == "R":
            self.__state.inactive_players[self.__state.inactive_players.index(candidate)] = player
        else:
            self.__state.active_players[self.__state.active_players.index(candidate)] = player
        self.__state.players_map.pop(name)
        self.__state.players_map[player.name] = player

    def __get_new_starters(self, period: int, size: int) -> list:
        """
         Returns the new starters given the unit size and the period

        Args:
            period (int): Period.
            size (int): Size.
        """
        new_starters = []
        if size > self.num_starters:
            indices = self.rotate_map[size][period]
            for i in indices:
                if i > len(self.__state.starters):
                    adjusted_index = i-1-self.num_starters
                    new_starter = self.__state.reserves[adjusted_index]
                else:
                    new_starter = self.__state.starters[i-1]
                new_starters.append(new_starter)
        else:
            new_starters = self.__state.starters.copy()
        return new_starters

    def __assign_with_alternative(self, target, player: Player,
                                  new_targets: dict,
                                  alternatives_available: dict) -> bool:
        """Assign player using an available alternative slot when target is occupied."""
        for alt_pos, alt_player in alternatives_available.items():
            if alt_pos not in new_targets:
                new_targets[alt_pos] = alt_player
                new_targets[target] = player
                return True
        return False

    def __assign_tuple_target(self, player: Player, target: tuple,
                              new_targets: dict,
                              alternatives_available: dict) -> bool:
        """Assign player for tuple targets, preferring first then second position."""
        pos1, pos2 = target
        if pos1 not in new_targets:
            new_targets[pos1] = player
            return True
        if pos2 not in new_targets:
            new_targets[pos2] = player
            return True
        return self.__assign_with_alternative(target, player,
                                              new_targets,
                                              alternatives_available)

    def __assign_single_target(self, player: Player, target: str,
                               new_targets: dict,
                               alternatives_available: dict) -> bool:
        """Assign player for single targets, falling back to alternative slots."""
        if target not in new_targets:
            new_targets[target] = player
            return True
        return self.__assign_with_alternative(target, player,
                                              new_targets,
                                              alternatives_available)

    def __collect_position_preferences(self) -> tuple:
        """Collect initial targets, alternatives, and swap candidates."""
        swappable = {}
        alternatives_available = {}
        new_targets = {}
        points = 0
        for player in self.__state.active_players:
            fav, alt = self.__get_position_choices(player_name=player.name)
            if player.position == fav:
                if fav not in new_targets:
                    new_targets[fav] = player
                if alt not in alternatives_available:
                    alternatives_available[alt] = player
                continue
            if player.position == alt:
                points += 1
                swappable[player] = fav
                continue
            points += 2
            swappable[player] = (fav, alt)
        return swappable, alternatives_available, new_targets, points

    def __reassign_swappables(self, swappable: dict,
                              alternatives_available: dict,
                              new_targets: dict) -> bool:
        """Try to assign each swappable player to a preferred target."""
        reassign = False
        for player, target in swappable.items():
            if isinstance(target, tuple):
                changed = self.__assign_tuple_target(player, target,
                                                     new_targets,
                                                     alternatives_available)
            else:
                changed = self.__assign_single_target(player, target,
                                                      new_targets,
                                                      alternatives_available)
            reassign = reassign or changed
        return reassign

    def __apply_targets(self, new_targets: dict) -> None:
        """Apply computed target positions to active players."""
        for player in self.__state.active_players:
            for new_pos, target_player in new_targets.items():
                if player == target_player:
                    player.position = new_pos

    def __validate_positions(self) -> None:
        """
        Rotates players

        Args:
            period (int): Period.
        """
        swappable, alternatives_available, new_targets, points = (
            self.__collect_position_preferences()
        )
        if points < len(self.__state.active_players) or not alternatives_available:
            return
        reassign = self.__reassign_swappables(swappable,
                                              alternatives_available,
                                              new_targets)
        if reassign:
            self.__apply_targets(new_targets)

    def rotate(self, period: int) -> None:
        """
        Rotates players

        Args:
            period (int): Period.
        """
        size = len(self.__state.starters) + len(self.__state.reserves)
        new_starters = self.__get_new_starters(period, size)
        if not self.__state.active_players:
            self.__state.active_players = new_starters
        else:
            for player in self.__state.active_players:
                if player not in new_starters:
                    self.__state.assigned_positions.pop(player.position)
                    player.position = "R"
                    self.__state.inactive_players.append(player)
        if not self.__state.inactive_players:
            self.__state.inactive_players = self.__state.reserves.copy()
        else:
            for player in new_starters:
                if player in self.__state.inactive_players:
                    player.position = self.__set_position(player.name)
                    self.__state.inactive_players.remove(player)
        self.__state.active_players = new_starters
        # for p in self.__active_players:
        #    print(f"1. {p.name} -> {p.position}")
        self.__validate_positions()
        # for p in self.__active_players:
        #    print(f"2. {p.name} -> {p.position}")

class Team:
    """
    Represents a team
    """

    def __init__(self, name: str, positions_db: dict):
        """
        Initializes a new Team object.

        Args:
            name (str): The team's name.
        """
        self.__name: str = name
        self.__players = []
        self.__goalkeeper = None
        self.__goalkeeper_reserve = []
        self.__defense: Unit = Unit("defense", ["LB", "CB", "RB"], positions_db)
        self.__offense: Unit = Unit("offense", ["LW", "ST", "RW"], positions_db)
        self.__players_map = {}

    @property
    def name(self) -> str:
        """The name of the team."""
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value:
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def players(self) -> list:
        """The list of players."""
        return self.__players

    def get_active_players(self) -> list:
        """The list of active players."""
        active_players = [self.__goalkeeper]
        active_players.extend(self.__defense.active_players)
        active_players.extend(self.__offense.active_players)
        return active_players

    def get_players(self) -> list:
        """The list of all players."""
        all_players = [self.__goalkeeper]
        all_players.extend(self.__defense.active_players)
        all_players.extend(self.__defense.inactive_players)
        all_players.extend(self.__offense.active_players)
        all_players.extend(self.__offense.inactive_players)
        return all_players


    def get_player_by_name(self, name: str) -> Player:
        """
        Returns a player given their name

        Args:
            name (str): The player's name.
        """
        return self.__players_map.get(name)

    def add_goalkeeper(self, player: Player) -> None:
        """
        Adds goalkeepers to the team

        Args:
            player (Player): The player to add.
        """
        if not self.__goalkeeper:
            if self.get_player_by_name(player.name):
                raise ValueError(f"Player {player.name} already added.")
            player.starting_position = "GK"
            player.position = "GK"
            self.__goalkeeper = player
            self.__players_map[player.name] = player
            # print(f"Adding {player.name} as {player.position}")
        else:
            if player not in self.__players and player != self.__goalkeeper:
                raise ValueError(f"Player {player.name} not part of the team.")
            self.__goalkeeper_reserve.append(player)

    def add_player(self, new_player: Player, unit_name: str) -> None:
        """
        Adds a new player to the team

        Args:
            new_player (Player): The player to add.
            unit_name (str): The unit's name where to add the player.
        """
        if new_player in self.__players:
            raise ValueError(f"Player {new_player.name} already in the team.")

        self.__players.append(new_player)
        self.__players_map[new_player.name] = new_player
        unit_map = {"defense": self.__defense, "offense": self.__offense}
        unit = unit_map.get(unit_name)
        unit.add_player(new_player)

    def swap(self, player_name1: str, player_name2: str) -> None:
        """
        Swaps players

        Args:
            player_name1 (str): Player to swap.
            player_name2 (str): Player to swap.
        """
        if self.__defense.get_player_by_name(player_name1):
            player1 = self.__defense.get_player_by_name(player_name1)
            player2 = self.__offense.get_player_by_name(player_name2)
            if not player2:
                if player_name2 != self.__goalkeeper.name:
                    raise ValueError(f"Player2 {player_name2} not in offense.")
                self.__defense.swap(player_name1, self.__goalkeeper)
                self.__swap_keeper(player1, True)
            else:
                positions = {"starting_position": player2.starting_position,
                             "position": player2.position}
                self.__defense.swap(player_name1, player2)
                self.__offense.swap(player_name2, player1, **positions)
        elif self.__offense.get_player_by_name(player_name1):
            player1 = self.__offense.get_player_by_name(player_name1)
            player2 = self.__defense.get_player_by_name(player_name2)
            if not player2:
                if player_name2 != self.__goalkeeper.name:
                    raise ValueError(f"Player2 {player_name2} not in defense.")
                self.__offense.swap(player_name1, self.__goalkeeper)
                self.__swap_keeper(player1, True)
            else:
                positions = {"starting_position": player2.starting_position,
                             "position": player2.position}
                self.__offense.swap(player_name1, player2)
                self.__defense.swap(player_name2, player1, **positions)
        else:
            # could it be goalkeeper
            if player_name1 != self.__goalkeeper.name:
                raise ValueError(f"Player to swap not found: {player_name1}.")
            player2 = self.__defense.get_player_by_name(player_name2)
            self.__swap_keeper(player2)

    def __swap_keeper(self, candidate: Player, force: bool = False) -> None:
        """
        Swaps goalkeeper

        Args:
            candidate (Player): The player to be swapped in.
            force (bool): Forces the swap even if candidate not in any unit.
        """
        if candidate != self.__goalkeeper:
            if self.__defense.get_player_by_name(candidate.name):
                self.__defense.swap(candidate.name, self.__goalkeeper)
            elif self.__offense.get_player_by_name(candidate.name):
                self.__offense.swap(candidate.name, self.__goalkeeper)
            else:
                if not force:
                    raise ValueError(f"Candidate {candidate.name} not in team.")

            candidate.position = "GK"
            self.__goalkeeper = candidate

    def rotate(self, period: int) -> None:
        """
        Rotates players

        Args:
            period (int): Period.
        """
        if period < 1 or period > 8:
            raise ValueError(f"Unexpected period {period}.")
        if period > 1 and period % 2 == 1:
            candidate = self.__goalkeeper_reserve.pop(0)
            self.__swap_keeper(candidate)
        self.__defense.rotate(period)
        self.__offense.rotate(period)

class Period:
    """
    Represents a period in a game
    """
    def __init__(self, number: int) -> None:
        """
        Initializes a new Period object.

        Args:
            number (int): The period's number.
        """
        self.__number = number
        self.__positions = {}

    @property
    def number(self) -> int:
        """The number of the period."""
        return self.__number

    @property
    def positions(self) -> dict:
        """The positions of the period."""
        return self.__positions

    def add_position(self, player_name: str, position: str) -> None:
        """
        Adds a player's position to the period

        Args:
            player_name (str): The name of the player.
            position (str): The position of the player.
        """
        self.__positions[player_name] = position

class Half:
    """
    Represents a half in a game
    """
    def __init__(self, number: int) -> None:
        """
        Initializes a new Half object.

        Args:
            number (int): The half's number.
        """
        self.__number = number
        self.__periods = []

    @property
    def number(self) -> int:
        """The number of the half."""
        return self.__number

    def add_period(self, period: Period) -> None:
        """
        Adds a period to the half

        Args:
            period (Period): The period to add.
        """
        self.__periods.append(period)

    def display(self) -> None:
        """
        Displays the half information.
        """
        print(f"Half {self.__number}")
        print(f"{'':<12}", end="")
        positions = {}
        for period in self.__periods:
            for player_name, position in period.positions.items():
                if player_name not in positions:
                    positions[player_name] = [position]
                else:
                    positions[player_name].append(position)
            if period.number % 4 == 1:
                print(f"{'Starting':<12}", end="")
            elif period.number % 4 == 2:
                print(f"{'1st sub':<12}", end="")
            elif period.number % 4 == 3:
                print(f"{'2nd sub':<12}", end="")
            else:
                print(f"{'3rd sub':<12}")
        for player_name, pos_list in positions.items():
            print(f"{player_name:<12}", end="")
            for pos in pos_list:
                print(f"{pos:<12}", end="")
            print("")

class Game:
    """
    Represents a game
    """
    def __init__(self) -> None:
        """
        Initializes a new Game object.
        """
        self.__halves = []

    def add_half(self, half: Half) -> None:
        """
        Adds a half to the game

        Args:
            half (Half): The half to add.
        """
        self.__halves.append(half)

    def display(self) -> None:
        """
        Displays the game information.
        """
        for half in self.__halves:
            half.display()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rotation")
    parser.add_argument("--players_file",
                        type=str,
                        required=True,
                        dest="players_file",
                        help="Path to players file")
    parser.add_argument("--num_periods",
                        type=int,
                        required=False,
                        dest="num_periods",
                        default=8,
                        help="Number of periods in the game")
    args = parser.parse_args()
    in_file = args.players_file
    with open(in_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        defense = data.get("defense", [])
        offense = data.get("offense", [])
        keepers = data.get("keepers", [])
        half_time_swaps = data.get("swaps", [])

    num_periods = args.num_periods
    team = Team("B4 Lions", load_positions())
    for defender_name in defense:
        defender_player = Player(defender_name)
        team.add_player(defender_player, "defense")
    for attacker_name in offense:
        attacker_player = Player(attacker_name)
        team.add_player(attacker_player, "offense")
    starting_keeper_name = keepers.pop(0)
    starting_keeper = Player(starting_keeper_name)
    team.add_goalkeeper(starting_keeper)
    for reserve_keeper_name in keepers:
        reserve_keeper = team.get_player_by_name(reserve_keeper_name)
        team.add_goalkeeper(reserve_keeper)

    new_game = Game()
    for period_number in range(1, num_periods+1):
        if period_number == 1:
            new_half = Half(1)
            new_game.add_half(new_half)
        if period_number == 5:
            new_half = Half(2)
            new_game.add_half(new_half)
            for swap in half_time_swaps:
                team.swap(swap[0], swap[1])
        team.rotate(period_number)
        new_period = Period(period_number)
        for team_player in team.get_players():
            new_period.add_position(team_player.name, team_player.position)
        new_half.add_period(new_period)
    new_game.display()
