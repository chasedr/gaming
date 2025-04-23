from typing import Tuple
import random
import threading
import time

from game_map import GameMap

class Entity(threading.Thread):
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        super().__init__()
        self.is_stop = False
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def random_move(self):
        # Randomly add or subtract values to x and y
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        self.move(dx, dy)

    def run(self):
        counter = 0
        # Implement the logic for the entity's behavior
        while self.is_stop == False:
            self.random_move()
            time.sleep(1)
            counter += 1
            if counter > 10:
                self.is_stop = True
                print(f"{self.char} stopped moving after 10 iterations.")

    def stop(self):
        # Stop the entity's behavior
        self.is_stop = True


class Person(Entity):
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int], name: str, game_map: GameMap):
        super().__init__(x, y, char, color)
        self.name = name
        self.game_map = game_map

    def introduce(self):
        print(f"Hello, my name is {self.name}.")

    def eyesight(self):
        # Implement the logic for the entity's behavior
        # For example, you can print the entity's position
        print(f"I am at position ({self.x}, {self.y}). --({self.name})")
        print(f"I see something interesting! --({self.name})")
        print(f"oh, that's {self.game_map.get_location_name(self.x, self.y)}")

    def random_see(self):
        self.eye_is_opened = random.choice([True, False])
        if self.eye_is_opened:
            self.eyesight()

    def run(self):
        counter = 0
        # Implement the logic for the entity's behavior
        while self.is_stop == False:
            self.random_move()
            self.random_see()
            time.sleep(1)
            counter += 1
            if counter > 10:
                self.is_stop = True
                print(f"{self.char} stopped moving after 10 iterations.")


class Ant(Entity):
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int], name: str, game_map: GameMap):
        super().__init__(x, y, char, color)
        self.name = name
        self.game_map = game_map

    def introduce(self):
        print(f"Hello, my name is {self.name}. I am an ant.")

    def run(self):
        counter = 0
        while self.is_stop == False:
            self.random_move()
            time.sleep(1)
            counter += 1
            if counter > 10:
                self.is_stop = True
                print(f"{self.char} stopped moving after 10 iterations.")

    #读取触角（文件），获取是否有食物或者障碍
    #写入足（文件），移动
    