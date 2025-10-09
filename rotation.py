"""
    This module provides utility functions for data processing.
    It includes functions for cleaning, transforming, and analyzing data.
"""

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
            new_player.position = "R"
            new_player.starting_position = new_player.position
            self.reserves.append(new_player)
        else:
            new_player.position = self.__positions[current_starters]
            new_player.starting_position = new_player.position
            self.__starters.append(new_player)
        self.__players_map[new_player.name] = new_player
        print(f"Adding {new_player.name} as {new_player.starting_position}")

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

    def rotate(self, period: int) -> None:
        """
        Rotates players

        Args:
            period (int): Period.
        """
        size = len(self.__starters) + len(self.__reserves)
        new_starters = self.__get_new_starters(period, size)
        inactive_positions = []
        if not self.__active_players:
            self.__active_players = new_starters
        else:
            for player in self.__active_players:
                if player not in new_starters:
                    inactive_positions.append(player.position)
                    player.position = "R"
                    self.__inactive_players.append(player)
        if not self.__inactive_players:
            self.__inactive_players = self.__reserves.copy()
        else:
            for player in new_starters:
                if player in self.__inactive_players:
                    player.position = inactive_positions.pop(-1)
                    self.__inactive_players.remove(player)
        self.__active_players = new_starters

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
            player.starting_position = "GK"
            player.position = "GK"
            self.__goalkeeper = player
            self.__players_map[player.name] = player
            print(f"Adding {player.name} as {player.position}")
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


def main():
    """ main """
    num_periods = 8
    # 9/27
    # defense = ["Arturo", "Asher", "Piero", "Teddy", "Brogan"]
    # offense = ["Ottavio", "William", "Anderson", "Stephen", "Winston"]
    # keepers = ["Charles", "Anderson", "Piero", "Stephen"]
    # half_time_swaps = [["Piero", "Ottavio"],["Brogan", "Anderson"]]
    # 10/11 - with Charles
    defense = ["Asher", "Arturo", "Anderson", "Piero"]
    offense = ["Brogan", "Daniel", "William", "Winston", "Teddy"]
    keepers = ["Charles", "Brogan", "Anderson", "Piero"]
    half_time_swaps = [["Teddy", "Anderson"], ["Brogan", "Piero"]]
    # 10/11 - without Charles
    # defense = ["Asher", "Teddy", "Piero"]
    # offense = ["Brogan", "Stephen", "Winston", "William"]
    # keepers = ["Anderson", "Brogan", "Anderson", "Stephen"]
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

    for period in range(1, num_periods+1):
        if period == 5 and half_time_swaps:
            for swap in half_time_swaps:
                team.swap(swap[0], swap[1])
        team.rotate(period)
        print(f"Period: {period}")
        for player in team.get_active_players():
            print(f"{player.position}: {player.name}")


if __name__ == "__main__":
    main()