import os
import pygame

class Assets:
    def __init__(self):
        self.rooms = {}
        self.load_rooms()

    def load_rooms(self):
        for filename in os.listdir("assets/rooms"):
            if filename.endswith(".png"):
                key = filename.replace(".png", "")
                img = pygame.image.load("assets/rooms/" + filename)
                img = pygame.transform.scale(img, (50,50))
                self.rooms[key] = img
