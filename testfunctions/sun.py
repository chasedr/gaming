import configparser
import random
import time
import logging
from datetime import datetime

class Sun:
    def __init__(self, config_file='sun.conf'):
        self.config = self.load_config(config_file)
        self.x = self.config.getint('SunPosition', 'x', fallback=100)
        self.y = self.config.getint('SunPosition', 'y', fallback=100)
        self.z = self.config.getint('SunPosition', 'z', fallback=1000)
        self.grid = {}  # Store lighting values for each block

    @staticmethod
    def load_config(config_file):
        config = configparser.ConfigParser()
        try:
            config.read(config_file)
        except Exception as e:
            logging.error(f"Error reading config file: {e}")
        return config

    def move(self):
        old_coords = (self.x, self.y, self.z)
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
        self.z += random.randint(-1, 1)
        new_coords = (self.x, self.y, self.z)
        logging.info(f"Sun moved from {old_coords} to {new_coords}")

    def update_lighting(self):
        dx_dy_pairs = [(dx, dy) for dx in range(-20, 21) for dy in range(-20, 21) if dx**2 + dy**2 <= 400]
        updates = []
        
        for dx, dy in dx_dy_pairs:
            block = (self.x + dx, self.y + dy)
            if block not in self.grid:
                self.grid[block] = 0
            self.grid[block] += 1
            updates.append(block)

    def run(self, cycles=1000, delay=1):
        for cycle in range(1, cycles + 1):
            logging.info(f"Cycle {cycle}")
            self.move()
            self.update_lighting()
            time.sleep(delay)

    def display_grid(self):
        logging.info("Final lighting values for blocks:")
        for block, lighting in self.grid.items():
            logging.info(f"Block {block}: Lighting {lighting}")

def setup_logging():
    logging.basicConfig(
        filename='sun.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

if __name__ == '__main__':
    setup_logging()
    sun = Sun()
    sun.run()
    sun.display_grid()
