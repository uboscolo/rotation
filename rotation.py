"""
    This module provides utility functions for data processing.
    It includes functions for cleaning, transforming, and analyzing data.
"""

POSITIONS = {"Piero": {"defense": {"favorite": "RB", "alternate": "LB"},
                       "offense": {"favorite": "RW", "alternate": "ST"}},
             "Asher": {"defense": {"favorite": "CB", "alternate": "LB"},
                       "offense": {"favorite": "RW", "alternate": "ST"}},
             "Teddy": {"defense": {"favorite": "LB", "alternate": "CB"},
                       "offense": {"favorite": "LW", "alternate": "RW"}},
             "Daniel": {"defense": {"favorite": "CB", "alternate": "RB"},
                        "offense": {"favorite": "ST", "alternate": "LW"}},
             "Cal": {"defense": {"favorite": "LB", "alternate": "RB"},
                     "offense": {"favorite": "LW", "alternate": "ST"}},
             "Chris": {"defense": {"favorite": "RB", "alternate": "LB"},
                       "offense": {"favorite": "RW", "alternate": "ST"}},
             "Anderson": {"defense": {"favorite": "RB", "alternate": "LB"},
                          "offense": {"favorite": "RW", "alternate": "LW"}},
             "Charles": {"defense": {"favorite": "LB", "alternate": "RB"},
                         "offense": {"favorite": "ST", "alternate": "RW"}},
             "Ottavio": {"defense": {"favorite": "LB", "alternate": "RB"},
                         "offense": {"favorite": "RW", "alternate": "LW"}},
             "Isaac": {"defense": {"favorite": "RB", "alternate": "LB"},
                       "offense": {"favorite": "RW", "alternate": "LW"}},
             "Brogan": {"defense": {"favorite": "RB", "alternate": "LB"},
                        "offense": {"favorite": "LW", "alternate": "RW"}},
            }

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

    def __init__(self, name: str, positions: list):
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
        self.__starters = []
        self.__reserves = []
        self.__active_players = []
        self.__inactive_players = []
        self.__players_map = {}
        self.__assigned_positions = {}

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
        return self.__starters

    @property
    def reserves(self) -> list:
        """The unit's reserves."""
        return self.__reserves

    @property
    def active_players(self) -> list:
        """The unit's active players."""
        return self.__active_players

    @property
    def inactive_players(self) -> list:
        """The unit's inactive players."""
        return self.__inactive_players

    def get_player_by_name(self, name: str) -> Player:
        """
        Returns a player given their name

        Args:
            name (str): The player's name.
        """
        return self.__players_map.get(name)

    def __get_position_choices(self, player_name: str):
        """
        Returns the position choices after looking up in the DB

        Args:
            player_name (str): The player's name.
        """
        units = POSITIONS.get(player_name)
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
        if favorite not in self.__assigned_positions:
            position = favorite
        elif alternate not in self.__assigned_positions:
            position = alternate
        else:
            # Player not in a choice position
            for pos in self.__positions:
                if pos not in self.__assigned_positions:
                    position = pos
        self.__assigned_positions[position] = player_name
        return position

    def add_player(self, new_player: Player) -> None:
        """
        Adds a new player to the unit

        Args:
            new_player (Player): The player to add.
        """
        if new_player in self.__starters or new_player in self.__reserves:
            raise ValueError(f"Player {new_player.name} already in the {self.__name} unit.")

        current_starters = len(self.__starters)
        if current_starters == self.num_starters:
            # Reserves
            new_player.position = "R"
            new_player.starting_position = new_player.position
            self.reserves.append(new_player)
        else:
            new_player.position = self.__set_position(new_player.name)
            new_player.starting_position = new_player.position
            self.__starters.append(new_player)
        self.__players_map[new_player.name] = new_player
        # print(f"Adding {new_player.name} as {new_player.starting_position}")

    def swap(self, name: str, player: Player, **positions) -> None:
        """
        Swaps players

        Args:
            name (str): The player's name to swap out
            player (Player): The player to swap in
        """
        candidate = self.__players_map.get(name)
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
            self.__reserves[self.__reserves.index(candidate)] = player
        else:
            self.__starters[self.__starters.index(candidate)] = player
        if position == "R":
            self.__inactive_players[self.__inactive_players.index(candidate)] = player
        else:
            self.__active_players[self.__active_players.index(candidate)] = player
        self.__players_map.pop(name)
        self.__players_map[player.name] = player

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
                if i > len(self.__starters):
                    adjusted_index = i-1-self.num_starters
                    new_starter = self.__reserves[adjusted_index]
                else:
                    new_starter = self.__starters[i-1]
                new_starters.append(new_starter)
        else:
            new_starters = self.__starters.copy()
        return new_starters
    
    def __validate_positions(self) -> None:
        """
        Rotates players

        Args:
            period (int): Period.
        """
        swappable = {}
        alternatives_available = {}
        new_targets = {}
        points = 0
        reassign = False
        for player in self.__active_players:
            # print(f"{player.name} - position: {player.position}")
            fav, alt = self.__get_position_choices(player_name=player.name)
            if player.position == fav:
                if fav not in new_targets:
                    new_targets[fav] = player
                if alt not in alternatives_available:
                    alternatives_available[alt] = player
            elif player.position == alt:
                points += 1
                swappable[player] = fav
            else:
                points += 2
                swappable[player] = (fav, alt)
        if points >= len(self.__active_players) and alternatives_available:
            for player, target in swappable.items():
                if isinstance(target, tuple):
                    pos1, pos2 = target
                    if pos1 in new_targets:
                        if pos2 in new_targets:
                            for alt_pos, alt_player in alternatives_available.items():
                                if alt_pos not in new_targets:
                                    new_targets[alt_pos] = alt_player
                                    new_targets[target] = player
                                    reassign = True
                                    break
                        else:
                            new_targets[pos2] = player
                            reassign = True
                    else:
                        new_targets[pos1] = player
                        reassign = True
                else:
                    if target not in new_targets:
                        new_targets[target] = player
                        reassign = True
                    else:
                        for alt_pos, alt_player in alternatives_available.items():
                            if alt_pos not in new_targets:
                                new_targets[alt_pos] = alt_player
                                new_targets[target] = player
                                reassign = True
                                break
        if reassign:
            for player in self.__active_players:
                for new_pos, target_player in new_targets.items():
                    if player == target_player:
                        player.position = new_pos

    def rotate(self, period: int) -> None:
        """
        Rotates players

        Args:
            period (int): Period.
        """
        size = len(self.__starters) + len(self.__reserves)
        new_starters = self.__get_new_starters(period, size)
        if not self.__active_players:
            self.__active_players = new_starters
        else:
            for player in self.__active_players:
                if player not in new_starters:
                    self.__assigned_positions.pop(player.position)
                    player.position = "R"
                    self.__inactive_players.append(player)
        if not self.__inactive_players:
            self.__inactive_players = self.__reserves.copy()
        else:
            for player in new_starters:
                if player in self.__inactive_players:
                    player.position = self.__set_position(player.name)
                    self.__inactive_players.remove(player)
        self.__active_players = new_starters
        # for p in self.__active_players:
        #    print(f"1. {p.name} -> {p.position}")
        self.__validate_positions()
        # for p in self.__active_players:
        #    print(f"2. {p.name} -> {p.position}")

class Team:
    """
    Represents a team
    """

    def __init__(self, name: str):
        """
        Initializes a new Team object.

        Args:
            name (str): The team's name.
        """
        self.__name: str = name
        self.__players = []
        self.__goalkeeper = None
        self.__goalkeeper_reserve = []
        self.__defense: Unit = Unit("defense", ["LB", "CB", "RB"])
        self.__offense: Unit = Unit("offense", ["LW", "ST", "RW"])
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

def main():
    """ main """
    num_periods = 8
    # Option 1 - 11 players
    defense = ["Asher", "Teddy", "Brogan", "Piero"]
    offense = ["Daniel", "Chris", "Isaac", "Ottavio", "Cal"]
    keepers = ["Anderson", "Isaac", "Brogan", "Isaac"]
    half_time_swaps = [["Ottavio", "Brogan"]]
    # half_time_swaps = []
    team = Team("B4 Lions")
    for name in defense:
        player = Player(name)
        team.add_player(player, "defense")
    for name in offense:
        player = Player(name)
        team.add_player(player, "offense")
    name = keepers.pop(0)
    player = Player(name)
    team.add_goalkeeper(player)
    for name in keepers:
        player = team.get_player_by_name(name)
        team.add_goalkeeper(player)

    new_game = Game()
    for period in range(1, num_periods+1):
        if period == 1:
            new_half = Half(1)
            new_game.add_half(new_half)
        if period == 5:
            new_half = Half(2)
            new_game.add_half(new_half)
            for swap in half_time_swaps:
                team.swap(swap[0], swap[1])
        team.rotate(period)
        new_period = Period(period)
        # print(f"Period: {period}")
        for player in team.get_players():
            # print(f"{player.position}: {player.name}")
            new_period.add_position(player.name, player.position)
        new_half.add_period(new_period)
    new_game.display()

if __name__ == "__main__":
    main()
