class BallPit:
    def __init__(self, player: bool, pit_type: str):
        self.ball_count = 0
        self.associated_player = player
        self.pit_type = pit_type

    def get_ball_count(self):
        return self.ball_count

    def add_ball(self, ball_count: int = 1):
        self.ball_count += ball_count
        return self.ball_count

    def empty_pit(self):
        if self.is_small():
            current_balls = self.ball_count
            self.ball_count = 0
            return current_balls
        else:
            raise TypeError("Cannot empty big pit during play")

    def match_player(self, player: bool):
        if player == self.associated_player:
            return True
        return False

    def is_small(self):
        if self.pit_type == "small":
            return True
        return False
