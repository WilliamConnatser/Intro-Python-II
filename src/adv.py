import random
import os
from room import Room
from player import Player

#
# Dictionary of rooms
# Declare all the rooms
#
rooms = {
    "outside": Room(
        room_id="outside",
        name="Outside Cave Entrance",
        description="North of you, the cave mount beckons",
        items=["torch","hatchet"]
    ),
    "foyer": Room(
        room_id="foyer",
        name="Foyer",
        description="Dim light filters in from the south. Dusty passages run north and east.",
        items=["matches","key"]
    ),
    "overlook": Room(
        room_id="overlook",
        name="Grand Overlook",
        description="A steep cliff appears before you, falling into the darkness. Ahead to the north, a light flickers in the distance, but there is no way across the chasm.",
        items=["key","gas"]
    ),
    "narrow": Room(
        room_id="narrow", 
        name="Narrow Passage", 
        description="The narrow passage bends here from west to north. The smell of gold permeates the air.",
        items=["gun","knife"]
    ),
    "treasure": Room(
        room_id="treasure", 
        name="Treasure Chamber",
        description="You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.",
        items=["gold","bitcoin"]
    ),
}

#
# Declare Players
#
players = [
    Player("Player 1", "outside"),
    Player("Player 2", "outside")
]

#
# Main Game
#
class Game:
    def __init__(self,max_columns,empty_rooms,rooms,players):
        self.rooms = rooms #Array of Room objects
        self.max_columns = max_columns #Max columns on matrix
        self.min_empty_rooms = empty_rooms #Minimum empty rooms
        self.map = [] #Initialize map matrix
        self.players = players #Array of Player objects

        self.turn = random.randrange(len(self.players)) #Randomize first turn
        self.current_player = self.players[self.turn] #Set current player

        self.generate_map() #Generate a randomized 2D Matrix contains the map
        self.current_room = self.rooms[self.current_player.room] #Set current room

        self.loop()

    def announce_turn(self):
        print(f"It's {self.current_player.name}'s turn... \n")
        print(self.current_room.description + "\n")

    def parse_input(self):
        print(f"You can move: {self.possible_moves()}")
        print(f"You can pick up: {self.current_room.items}")
        print(f"Your inventory contains: {self.current_player.inventory}\n")
        print("1. Type q to quit")
        print("2. Type in the direction you want to head")
        print("3. Type in the item you want to pickup")
        print("4. Type in the item you want to drop\n")
        action = input(f"What would you like to do? >> ")
        action = action.strip().lower()

        if action == 'q':
            exit()
        elif action in self.current_room.items:
            self.players[self.turn].pickup(action)
            self.rooms[self.current_player.room].items.remove(action)
            self.increment_turn()
            self.loop()
        elif action in self.current_player.inventory:
            self.players[self.turn].drop(action)
            self.rooms[self.current_player.room].items.append(action)
            self.increment_turn()
            self.loop()
        elif self.valid_direction(action):
            self.players[self.turn].move(self.adjacent_rooms()[action])
            self.increment_turn()
            self.loop()
        else:
            self.loop()

    def valid_direction(self, direction):
        if direction in ["north", "south", "east", "west"] and self.adjacent_rooms()[direction] != None:
            return True
        return False

    def increment_turn(self):
        if self.turn != len(self.players)-1:
            self.turn += 1
        else:
            self.turn = 0

        self.current_player = self.players[self.turn] #Set current player
        self.current_room = self.rooms[self.current_player.room] #Set current room

    def loop(self):
        os.system('clear')
        self.print_map(self.current_player)
        print("\n\n")
        self.announce_turn()
        self.parse_input()

    def generate_map(self):

        rooms = list(self.rooms.keys()) + ([None] * self.min_empty_rooms)
        if len(rooms) % self.max_columns != 0:
            rooms = rooms + ([None] * len(rooms) % self.max_columns)

        #Initialize map matrix rows
        for x in range(len(rooms)//self.max_columns):
            self.map.append([])

        print(rooms)

        #Insert random rooms into the map matrix columns
        for x in range(len(self.map)):
            for banana in range(self.max_columns):
                rand_index = random.randint(0, len(rooms)-1)
                self.map[x].append(rooms[rand_index])

                if rooms[rand_index] != None:
                    #Set row and column on each room object
                    self.rooms[rooms[rand_index]].row = x
                    self.rooms[rooms[rand_index]].column = self.map[x].index(rooms[rand_index])

                rooms.remove(rooms[rand_index])
        print(self.map)

    def possible_moves(self):
        if not hasattr(self.rooms[self.current_room.id], 'possible_moves'):
            self.rooms[self.current_room.id].possible_moves = self.adjacent_rooms()

        return f"{[direction for direction in self.rooms[self.current_room.id].possible_moves if self.rooms[self.current_room.id].possible_moves[direction] != None]}"

    def adjacent_rooms(self):
        if not hasattr(self.rooms[self.current_room.id], 'adjacent_rooms'):
            print(self.current_room)
            if self.current_room.row - 1 > -1:
                north = self.map[self.current_room.row - 1][self.current_room.column]
            else:
                north = None

            if self.current_room.column + 1 < len(self.map[0]):
                east = self.map[self.current_room.row][self.current_room.column + 1]
            else:
                east = None

            if self.current_room.column - 1 > -1:
                west = self.map[self.current_room.row][self.current_room.column - 1]
            else:
                west = None
            
            if self.current_room.row + 1 < len(self.map):
                south = self.map[self.current_room.row + 1][self.current_room.column]
            else:
                south = None
        
            self.rooms[self.current_room.id].adjacent_rooms = {
                "north": north,
                "east": east,
                "west": west,
                "south": south
            }
        
        return self.rooms[self.current_room.id].adjacent_rooms

    def print_map(self,current_player):
        space = " "
        you = "YOU"
        bottom = "_"
        top = ""

        for column in range(self.max_columns):
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
                elif column == current_player.room:
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

    @staticmethod
    def print_centered(text):
        print(text.center(os.get_terminal_size().columns))

game = Game(2,1,rooms,players)

# Write a loop that:
#
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.

# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
