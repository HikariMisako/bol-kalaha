class BallPit:
    """
    Ball pit to hold 'balls' in. No ball objects are created, they are only counted.
    """

    def __init__(self, player: bool, pit_type: str):
        self.ball_count = 0
        self.associated_player = player
        self.pit_type = pit_type

    def __str__(self):
        """
        Quick-read print formatting
        :return: string with large/small pit info, current ball count and associated player
        """
        if self.is_large():
            return f"Large pit with {self.get_ball_count()} balls, associated player {self.associated_player}"
        return f"Small pit with {self.get_ball_count()} balls, associated player {self.associated_player}"

    def short_str(self) -> str:
        return_str = ""
        if self.is_large():
            return_str += "L"
        player = "1"
        if not self.associated_player:
            player = "2"
        return_str += f"P{player}-{self.get_ball_count()}"
        return return_str

    def get_ball_count(self) -> int:
        """
        :return: current number of balls in this ball pit
        """
        return self.ball_count

    def add_ball(self, ball_count: int = 1) -> int:
        """
        Add one or more balls to the ball pit.
        :param ball_count: number of balls to add.
        :return: resulting number of balls in the pit.
        """
        if ball_count < 1:
            raise ValueError("ball_count needs to be an integer above zero!")
        self.ball_count += ball_count
        return self.ball_count

    def empty_pit(self) -> int:
        """
        Removes all the balls in the pit, if the pit is small.
        :return: The number of balls that were in the pit before emptying.
        """
        # note that is_playable would be the wrong check,
        # one player can empty the opposite player's pit if they land on an empty pit of their own
        if self.is_small():
            current_balls = self.ball_count
            self.ball_count = 0
            return current_balls
        else:
            raise ValueError("Cannot empty big pit during play")

    def match_player(self, player: bool) -> bool:
        """
        Checks if the input player is the player associated with this ball pit.
        :param player: player to check against the associated player
        :return: True if matched, false if not.
        """
        if player == self.associated_player:
            return True
        return False

    def is_small(self) -> bool:
        """
        Checks whether this pit is a small pit or not.
        :return: True if small, False otherwise
        """
        if self.pit_type == "small":
            return True
        return False

    def is_large(self) -> bool:
        """
        Checks whether this pit is a large pit or not.
        :return: True if large, False otherwise
        """
        return not self.is_small()

    def is_playable(self, player: bool) -> bool:
        """
        Checks whether the given player can play balls from this pit.
        :return:
        """
        if not self.match_player(player):
            raise ValueError("this pit does not belong to this player!")
        if self.get_ball_count() <= 0:
            raise ValueError("this pit is empty!")
        if self.is_large():
            raise ValueError("the scoring pit cannot be played!")
        return True
