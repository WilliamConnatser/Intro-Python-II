# Write a class to hold player information, e.g. what room they are in
# currently.
class Player:
    def __init__(self,name,room):
        self.name = name
        self.room = room
        self.inventory = []

    def move(self,room):
        self.room = room

    def pickup(self, item):
        self.inventory.append(item)

    def drop(self, item):
        self.inventory.remove(item)