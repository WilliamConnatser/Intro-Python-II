from random import randrange
from room import Room
from player import Player
import os

#
# Dictionary of rooms
# Declare all the rooms
#
rooms = {
    "outside": Room(name="Outside Cave Entrance", description="North of you, the cave mount beckons", items=["torch","hatchet"]),

    "foyer": Room(name="Foyer", description="Dim light filters in from the south. Dusty passages run north and east.", items=["matches","key"]),

    "overlook": Room(name="Grand Overlook", description="A steep cliff appears before you, falling into the darkness. Ahead to the north, a light flickers in the distance, but there is no way across the chasm.", items=["key","gas"]),

    "narrow": Room(name="Narrow Passage", description="The narrow passage bends here from west to north. The smell of gold permeates the air.", items=["gun","knife"]),

    "treasure": Room(name="Treasure Chamber", description="You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.", items=["gold","bitcoin"]),
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
players = [
    Player("Player 1", "outside")
]

#
# Main Game
#
class Game:
    def __init__(self,map,rooms,players):
        self.map = map
        self.rooms = rooms
        self.players = players
        self.turn = randrange(len(self.players))
        self.loop()

    def announce_turn(self):
        player = self.players[self.turn]
        print(f"It's {player.name}'s turn... \n")
        print(self.rooms[player.room].description + "\n")

    def get_possible_moves(self):
        possible_moves = self.determine_possible_moves()     
        return f"{[direction for direction in possible_moves if possible_moves[direction] != None]}"

    def get_location_index(self):
        current_location = self.players[self.turn].room
        row_index, column_index = 0, 0

        for row in self.map:
            if current_location in row:
                column_index = row.index(current_location)
                row_index = self.map.index(row)
                break

        return {
            "row": row_index,
            "column": column_index
        }

    def determine_possible_moves(self):
        matrix_index = self.get_location_index()

        if matrix_index["row"] - 1 > -1:
            north = self.map[matrix_index["row"] - 1][matrix_index["column"]]
        else:
            north = None

        if matrix_index["column"] + 1 < len(self.map[0]):
            east = self.map[matrix_index["row"]][matrix_index["column"] + 1]
        else:
            east = None

        if matrix_index["column"] - 1 > -1:
            west = self.map[matrix_index["row"]][matrix_index["column"] - 1]
        else:
            west = None
        
        if matrix_index["row"] + 1 < len(self.map):
            south = self.map[matrix_index["row"] + 1][matrix_index["column"]]
        else:
            south = None
        
        return {
            "north": north,
            "east": east,
            "west": west,
            "south": south
        }

    def parse_input(self):
        print(f"You can move: {self.get_possible_moves()}")
        print(f"You can pick up: {self.rooms[self.players[self.turn].room].items}")
        print(f"Your inventory contains: {self.players[self.turn].inventory}\n")
        print("1. Type q to quit")
        print("2. Type in the direction you want to head")
        print("3. Type in the item you want to pickup")
        print("4. Type in the item you want to drop\n")
        action = input(f"What would you like to do? >> ")
        action = action.strip().lower()

        if action == 'q':
            exit()
        elif action in self.rooms[self.players[self.turn].room].items:
            self.players[self.turn].pickup(action)
            self.rooms[self.players[self.turn].room].items.remove(action)
            self.increment_turn()
            self.loop()
        elif action in self.players[self.turn].inventory:
            self.players[self.turn].drop(action)
            self.rooms[self.players[self.turn].room].items.append(action)
            self.increment_turn()
            self.loop()
        elif self.validate_input(action):
            self.players[self.turn].move(self.determine_possible_moves()[action])
            self.increment_turn()
            self.loop()
        else:
            self.loop()

    def validate_input(self, direction):
        if direction in ["north", "south", "east", "west"] and self.determine_possible_moves()[direction] != None:
            return True
        return False

    def increment_turn(self):
        if self.turn != len(self.players)-1:
            self.turn += 1
        else:
            self.turn = 0

    def print_map(self):
        space = " "
        you = "YOU"
        bottom = "_"
        top = ""

        for column in self.map[0]:
            top += f"[{bottom.center(50, '_')}]"

        self.print_centered(top)

        for row in self.map:
            line1 = ""
            line2 = ""
            line3 = ""
            line4 = ""
            line5 = ""

            for column in row:
                if column == None:
                    line1 += f"[{space.center(50, ' ')}]"
                    line2 += f"[{space.center(50, ' ')}]"
                    line3 += f"[{space.center(50, ' ')}]"
                    line4 += f"[{space.center(50, ' ')}]"
                    line5 += f"[{bottom.center(50, '_')}]"
                elif column == self.players[self.turn].room:
                    line1 += f"[{space.center(50, ' ')}]"
                    line2 += f"[{rooms[column].name.center(50, ' ')}]"
                    line3 += f"[{str(rooms[column].items).center(50, ' ')}]"
                    line4 += f"[{you.center(50, ' ')}]"
                    line5 += f"[{bottom.center(50, '_')}]"
                else:
                    line1 += f"[{space.center(50, ' ')}]"
                    line2 += f"[{rooms[column].name.center(50, ' ')}]"
                    line3 += f"[{space.center(50, ' ')}]"
                    line4 += f"[{space.center(50, ' ')}]"
                    line5 += f"[{bottom.center(50, '_')}]"

            self.print_centered(line1)
            self.print_centered(line2)
            self.print_centered(line3)
            self.print_centered(line4)
            self.print_centered(line5)

        print("\n\n")


    def loop(self):
        os.system('clear')
        self.print_map()
        self.announce_turn()
        self.parse_input()

    @staticmethod
    def print_centered(text):
        print(text.center(os.get_terminal_size().columns))

game = Game(map,rooms,players)

# Write a loop that:
#
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.

# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
