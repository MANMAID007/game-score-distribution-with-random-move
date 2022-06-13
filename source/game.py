import random

# class to generate game stage
class The_Game:
    def __init__(self, n=3, iter_len=1000, turn_multiplier=1, coin_multiplier=5):
        self.n = n
        self.iter_len = iter_len
        self.turn_multiplier = turn_multiplier
        self.coin_multiplier = coin_multiplier
    
    def death_rules(self, pos, barrier_list):
        if pos in barrier_list:
            return True
        else:
            return False
    
    def barrier_generator(self):
        n_barriers = random.choice(range(1, self.n))
        return random.sample(range(self.n), k=n_barriers)
    
    def boost_generator(self):
        return random.choice(range(self.n))
    
    def coin_generator(self):
        n_coins = random.choice(range(1, self.n + 1))
        return random.sample(range(self.n), k=n_coins)
    
    def point_calculator(self, pos, barrier_list, boost, coin_list):
        points = 0
        if pos in barrier_list:
            return points
        if pos == boost:
            points += (len(coin_list) * self.coin_multiplier + self.turn_multiplier)
        elif pos != boost and pos in coin_list:
            points += (self.coin_multiplier + self.turn_multiplier)
        else:
            points += self.turn_multiplier
        return points
    
    def stage_generator(self):
        barrier_indicators = random.sample(range(self.iter_len), k=random.choice(range(self.iter_len)))
        boost_indicators = random.sample(range(self.iter_len), k=random.choice(range(self.iter_len)))
        coin_indicators = random.sample(range(self.iter_len), k=random.choice(range(self.iter_len)))

        barriers = [self.barrier_generator() if i in barrier_indicators else [] for i in range(self.iter_len)]
        boosts = [self.boost_generator() if i in boost_indicators else None for i in range(self.iter_len)]
        coins = [self.coin_generator() if i in coin_indicators else [] for i in range(self.iter_len)]

        return barriers, boosts, coins
    
    def run(self, agent_move):
        br, bt, c = self.stage_generator()
        total_point = 0
        for i in range(self.iter_len):
            total_point += self.point_calculator(agent_move[i], br[i], bt[i], c[i])
            is_dead = self.death_rules(agent_move[i], br[i])
            if is_dead:
                break
        return total_point, is_dead

# this function runs the game
def run_game(n=5, iter_len=10):
    game = The_Game(n, iter_len)
    final_point = 0
    is_dead = False
    while not is_dead:
        agent_move = [random.choice(range(n)) for i in range(iter_len)]
        total_point, is_dead = game.run(agent_move)
        final_point += total_point
    return final_point