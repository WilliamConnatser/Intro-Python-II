import random
from room import Room
from player import Player

#
# Dictionary of rooms
# Declare all the rooms
#
rooms = {
    "outside": Room(name="Outside Cave Entrance", description="North of you, the cave mount beckons"),

    "foyer": Room(name="Foyer", description="""Dim light filters in from the south. Dusty
passages run north and east."""),

    "overlook": Room(name="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    "narrow": Room(name="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    "treasure": Room(name="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

#
# Map list matrix
# Links rooms together
#
map = [
    ["outside", None],
    ["foyer", "narrow"],
    ["overlook", "treasure"]
]

# room['outside'].n_to = room['foyer']
# room['foyer'].s_to = room['outside']
# room['foyer'].n_to = room['overlook']
# room['foyer'].e_to = room['narrow']
# room['overlook'].s_to = room['foyer']
# room['narrow'].w_to = room['foyer']
# room['narrow'].n_to = room['treasure']
# room['treasure'].s_to = room['narrow']

#
# Declare Players
#
players = {
    "player1": Player("Player 1", "outside")
}

#
# Main Game
#
class Game:
    def __init__(self,map,rooms,players):
        self.map = map
        self.rooms = rooms
        self.players = players        
        self.turn = random.choice(list(players.keys()))
        self.loop()

    def announce_turn(self):
        print(f"It's {self.turn}'s turn...")

    def announce_location(self):
        player = self.players[self.turn]
        print(f"{self.turn} is in the {player.room}")
        print(rooms[player.room].description)

    def announce_possibilities(self):
        possibilities = self.get_possibilities()     
        print(f"Possible Moves {[direction for direction in possibilities if possibilities[direction] != None]}")

    def get_location_index(self):
        current_location = self.players[self.turn].room;
        row_index, column_index = 0, 0

        for row in self.map:
            for column in row:
                if column == current_location:
                    break
                column_index += 1
            if self.map[column_index][row_index] != None:
                break
            row_index += 1

        return {
            "row": row_index,
            "column": column_index
        }

    def get_possibilities(self):
        matrix_index = self.get_location_index()
        north = self.map[matrix_index["column"] - 1][matrix_index["row"]]
        east = self.map[matrix_index["column"]][matrix_index["row"] + 1]
        west = self.map[matrix_index["column"]][matrix_index["row"] - 1]
        south = self.map[matrix_index["column"] + 1][matrix_index["row"]]
        return {
            "north": north,
            "east": east,
            "west": west,
            "south": south
        }

    def accept_input(self):
        print("jaa")

    def loop(self):
        self.announce_turn()
        self.announce_location()
        self.announce_possibilities()


game = Game(map,rooms,players)

# Write a loop that:
#
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.

# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
