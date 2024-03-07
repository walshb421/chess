class Game:
    def __init__(self):
        self.players = {}
        self.moves = []
        self.board = {}
        self.turn = -1
        self.chats = []
        self.messages = {
            "move": lambda object : self.on_move(object)
        }

    def on_message(self, message):
        if type(message) is dict:
            for key, value in message.items():
                self.messages[key](value)

    def on_move(move):
        print(move, flush=True)
        
	
    

