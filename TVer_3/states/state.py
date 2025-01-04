class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None # what state is bellow the current state

    def update(self, delta_time, actions): 
        pass
    def render(self, surface): # surface is the game canvas
        pass

    def enter_state(self): # essentailly the push
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1] # [-1] accessing the last element
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()