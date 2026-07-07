import random
"""
这个模块定义了一个`Person`类，用于模拟一个具有各种行为和能量传递机制的人。
一个`Person`可以向外释放能量，同样可以从外界接收能量，但是能量往往不能直接接收，
而是通过内部的器官转换成能量。释放能量也是一样的，是通过器官来释放能量。
这个类还包含了一些行为，例如社交行为、消费行为、运动行为、为了填饱肚子的行为、环境影响等。
能量是本源的物质，可以被直接修改，同时也可以通过行为来改变。
"""
import json
import threading
import time
import random
import os
import glob




class SkinInterface:
    def apply_substance(self, substance):
        raise NotImplementedError("This method should be overridden by subclasses")
    
# 肺部接口
# 眼睛接口 不是持续打开接收窗口的，外界只有在特定时间（由眼皮定时的打开/关闭）才能输入信息
# 耳朵接口 是持续打开接收窗口的，外界可以随时输入信息
# 鼻子接口 不是持续打开接收窗口的，外界只有在特定时间（由肺定时的打开/关闭）才能输入信息
# 嘴巴接口 不是持续打开接收窗口的，外界只有在特定时间（由嘴巴定时的打开/关闭）才能输入信息

class Leg:
    def __init__(self, length=1.0, strength=1.0):
        """
        Initialize a Leg instance.

        Args:
            length (float): The length of the leg (default is 1.0).
            strength (float): The strength of the leg (default is 1.0).
        """
        self.length = length
        self.strength = strength

    def kick(self, force):
        """
        Perform a kick with a specified force.

        Args:
            force (float): The force of the kick.

        Returns:
            None
        """
        if force <= self.strength:
            print(f"The leg performs a kick with a force of {force}.")
        else:
            print("The force exceeds the leg's strength. The kick is not successful.")

    def walk(self, distance):
        """
        Simulate walking a certain distance and return random XYZ coordinates
        whose sum equals the distance.

        Args:
            distance (float): The total distance to distribute.

        Returns:
            tuple: (x, y, z) where x + y + z == distance, each >= 0 if distance >= 0.
        """
        if distance < 0:
            # For negative distance, allow negative coordinates by symmetry
            # Generate two random numbers in [distance, 0] (since distance < 0)
            x = random.uniform(distance, 0)
            y = random.uniform(distance - x, 0)  # ensure z will be <= 0
            z = distance - x - y
        else:
            # Generate x in [0, distance], then y in [0, distance - x]
            x = random.uniform(0, distance)
            y = random.uniform(0, distance - x)
            z = distance - x - y

        return (x, y, z)

    def jump(self, height):
        """
        Simulate jumping to a certain height.

        Args:
            height (float): The height to jump.

        Returns:
            None
        """
        if height <= self.strength:
            print(f"The leg jumps to a height of {height} meters.")
        else:
            print("The height exceeds the leg's strength. The jump is not successful.")

    
    move = walk


class Eye:
    def __init__(self, color="brown", vision=1.0):
        """
        Initialize an Eye instance.

        Args:
            color (str): The color of the eye (default is "brown").
            vision (float): The vision clarity of the eye (default is 1.0, where 1.0 is normal vision).
        """
        self.color = color
        self.vision = vision
        self.is_open = False

    def open_eye(self):
        """
        Open the eye to allow receiving visual information.

        Returns:
            None
        """
        self.is_open = True
        print("The eye is now open.")

    def close_eye(self):
        """
        Close the eye to stop receiving visual information.

        Returns:
            None
        """
        self.is_open = False
        print("The eye is now closed.")

    def blink(self):
        """
        Simulate a blink by closing and then opening the eye.

        Returns:
            None
        """
        self.close_eye()
        self.open_eye()
        print("The eye blinked.")

    def see(self, x, y, z):
        """
        读取 world/ 中的所有 JSON 文件，比对物体坐标与当前位置的距离。
        如果距离小于 2，则打印出看到了什么。

        Args:
            x (float): 观察者的 x 坐标。
            y (float): 观察者的 y 坐标。
            z (float): 观察者的 z 坐标。

        Returns:
            None
        """
        if not self.is_open:
            print("The eye is closed and cannot see anything.")
            return

        world_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world')
        pattern = os.path.join(world_dir, '*.json')
        seen_names = []

        for filepath in sorted(glob.glob(pattern)):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue

            objects = data.get('objects', [])
            for obj in objects:
                ox = obj.get('x', 0)
                oy = obj.get('y', 0)
                oz = obj.get('z', 0)
                dx = x - ox
                dy = y - oy
                dz = z - oz
                distance = (dx*dx + dy*dy + dz*dz) ** 0.5
                if distance < 2:
                    name = obj.get('name', '未知物体')
                    seen_names.append(name)

        if seen_names:
            seen_str = '，'.join(seen_names)
            print(f"看到了{seen_str}", x,y,z)
        else:
            print("什么都没看到", x,y,z)

class Ear:
    def __init__(self, sensitivity=1.0):
        """
        Initialize an Ear instance.

        Args:
            sensitivity (float): The sensitivity of the ear (default is 1.0, where 1.0 is normal sensitivity).
        """
        self.sensitivity = sensitivity
        self.is_listening = True

    def start_listening(self):
        """
        Enable the ear to start listening.

        Returns:
            None
        """
        self.is_listening = True
        print("The ear is now listening.")

    def stop_listening(self):
        """
        Disable the ear from listening.

        Returns:
            None
        """
        self.is_listening = False
        print("The ear has stopped listening.")

    def hear(self, sound):
        """
        Simulate hearing a sound if the ear is listening.

        Args:
            sound (str): A description of the sound being heard.

        Returns:
            None
        """
        if self.is_listening:
            print(f"The ear hears: {sound}.")
        else:
            print("The ear is not listening and cannot hear anything.")



class Mouse:
    def __init__(self, dpi=800, buttons=3):
        """
        Initialize a Mouse instance.

        Args:
            dpi (int): The sensitivity of the mouse in dots per inch (default is 800).
            buttons (int): The number of buttons on the mouse (default is 3).
        """
        self.dpi = dpi
        self.buttons = buttons
        self.position = (0, 0)  # Initial position of the mouse

    def move(self, x, y):
        """
        Move the mouse to a new position.

        Args:
            x (int): The x-coordinate to move to.
            y (int): The y-coordinate to move to.

        Returns:
            None
        """
        self.position = (x, y)
        print(f"Mouse moved to position: {self.position}")

    def click(self, button="left"):
        """
        Simulate a mouse button click.

        Args:
            button (str): The button to click ('left', 'right', 'middle').

        Returns:
            None
        """
        print(f"Mouse {button} button clicked.")

    def scroll(self, direction="up"):
        """
        Simulate scrolling the mouse wheel.

        Args:
            direction (str): The direction to scroll ('up' or 'down').

        Returns:
            None
        """
        print(f"Mouse scrolled {direction}.")

class Nose:
    def __init__(self, sensitivity=1.0):
        """
        Initialize a Nose instance.

        Args:
            sensitivity (float): The sensitivity of the nose (default is 1.0, where 1.0 is normal sensitivity).
        """
        self.sensitivity = sensitivity
        self.is_smelling = False

    def start_smelling(self):
        """
        Enable the nose to start smelling.

        Returns:
            None
        """
        self.is_smelling = True
        print("The nose is now smelling.")

    def stop_smelling(self):
        """
        Disable the nose from smelling.

        Returns:
            None
        """
        self.is_smelling = False
        print("The nose has stopped smelling.")

    def smell(self, scent):
        """
        Simulate smelling a scent if the nose is enabled.

        Args:
            scent (str): A description of the scent being smelled.

        Returns:
            None
        """
        if self.is_smelling:
            print(f"The nose smells: {scent}.")
        else:
            print("The nose is not smelling and cannot detect any scent.")

class Memory:
    def __init__(self):
        """
        Initialize a Memory instance with an empty list to store memories.
        """
        self.memories = []

    def store_memory(self, memory):
        """
        Store a memory in the memory list.

        Args:
            memory (str): The memory to store.

        Returns:
            None
        """
        self.memories.append(memory)
        print(f"Memory stored: {memory}")

    def recall_memory(self, index):
        """
        Recall a memory by its index.

        Args:
            index (int): The index of the memory to recall.

        Returns:
            str: The recalled memory, or a message if the index is invalid.
        """
        if 0 <= index < len(self.memories):
            return self.memories[index]
        else:
            return "Memory not found."

    def forget_memory(self, index):
        """
        Forget a memory by its index.

        Args:
            index (int): The index of the memory to forget.

        Returns:
            None
        """
        if 0 <= index < len(self.memories):
            forgotten = self.memories.pop(index)
            print(f"Memory forgotten: {forgotten}")
        else:
            print("Memory not found.")


class Person(SkinInterface, threading.Thread):
    def __init__(self, json_file_path):
        threading.Thread.__init__(self)
        # 读取 JSON 数据
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        # 现在 data 已定义，可以安全使用
        self.wood = data.get('wood', 20.0)
        self.fire = data.get('fire', 20.0)
        self.earth = data.get('earth', 20.0)
        self.metal = data.get('metal', 20.0)
        self.water = data.get('water', 20.0)
        self.x = data.get('x', 0)
        self.y = data.get('y', 0)
        self.z = data.get('z', 0)
        self.vertical_angle = data.get('vertical_angle', 0.0)
        self.horizontal_angle = data.get('horizontal_angle', 0.0)
        self.density = data.get('density', 1.0)
        self.temperature = data.get('temperature', 37.0)
        self.environment_temperature = data.get('environment_temperature', 20.0)
        self.name = data.get('name', 'Unknown')
        self.age = data.get('age', 0)
        self.gender = data.get('gender', 'Unknown')
        self.substances = {}
        # 转移速率（请确保 JSON 中有这些值，否则用默认值）
        self.wood_out = data.get('wood_out', 1)
        self.fire_in = data.get('fire_in', 1)
        self.fire_out = data.get('fire_out', 1)
        self.earth_in = data.get('earth_in', 1)
        self.earth_out = data.get('earth_out', 1)
        self.metal_in = data.get('metal_in', 1)
        self.metal_out = data.get('metal_out', 1)
        self.water_in = data.get('water_in', 1)
        self.water_out = data.get('water_out', 1)
        self.wood_in = data.get('wood_in', 1)
        self.leg = Leg()
        self.eye = Eye()

    def run(self):
        while True:
            print(self.name)
            random_bool = random.choice([True, False])
            if random_bool:
                dx, dy, dz = self.leg.move(1)  # 每次循环走 1 米
                self.x += dx
                self.y += dy
                self.z += dz
                self.wood -= 1 # 每次走路消耗 1 单位木能量
            random_bool = random.choice([True, False])
            if random_bool:
                self.eye.blink()
                self.eye.see(self.x, self.y, self.z) # 每次循环尝试看周围的物体
                # 看到物体后，如果这个物体的能量叠加到自己身上能让自己的能量平衡，则增加到自己的喜欢列表上
                # 看到物体后，如果这个物体的能量叠加到自己身上能让自己的能量不平衡，则增加到自己的讨厌列表上
                # 看到喜欢的物体，根据程度，选择是否去接触这个物体，接触后能量会增加到自己身上
                # 看到讨厌的物体，根据程度，选择是否去躲避
                
            #self.transfer_energy()
            time.sleep(1)
            
    def apply_substance(self, substance):
        """
        Apply a given substance to the person. If the substance is already present,
        increment its count. Otherwise, add the substance with a count of 1.

        Args:
            substance (str): The name of the substance to apply.

        Returns:
            None
        """
        if substance in self.substances:
            self.substances[substance] += 1
        else:
            self.substances[substance] = 1
        print(f"{self.name} has applied {substance}. Current substances: {self.substances}")
    
    def apply_external_substance(self, external_class, substance):
        """
        Apply a given substance to the person and also notify an external class.

        Args:
            external_class (object): The external class instance that has an apply_substance method.
            substance (str): The name of the substance to apply.

        Returns:
            None
        """
        self.apply_substance(substance)
        external_class.apply_substance(substance)
        print(f"{self.name} has applied {substance} and notified the external class.")

    def modify_energy(self, element, amount):
        """
        Modify the energy level of a given element.

        Args:
            element (str): The element type ('wood', 'fire', 'earth', 'metal', 'water').
            amount (float): The amount of energy to modify (can be positive or negative).

        Returns:
            None
        """
        if hasattr(self, element):
            current_energy = getattr(self, element)
            setattr(self, element, current_energy + amount)
            print(f"{self.name}'s {element} energy modified by {amount}. New level: {getattr(self, element)}")
        else:
            print(f"Invalid element: {element}")

    def release_energy(self, element, amount):
        """
        Release a specified amount of energy of a given element to the environment.

        Args:
            element (str): The element type ('wood', 'fire', 'earth', 'metal', 'water').
            amount (float): The amount of energy to release.

        Returns:
            None
        """
        if hasattr(self, element):
            current_energy = getattr(self, element)
            if current_energy >= amount:
                external_class.modify_energy(element, -amount)
                print(f"{self.name} has released {amount} units of {element} energy.")
            else:
                print(f"{self.name} does not have enough {element} energy to release.")
        else:
            print(f"Invalid element: {element}")


    def transfer_energy(self):
        # Example energy transfer: 木 -> 火 -> 土 -> 金 -> 水 -> 木
        self.wood -= self.wood_out
        self.fire += self.fire_in
        self.fire -= self.fire_out
        self.earth += self.earth_in
        self.earth -= self.earth_out
        self.metal += self.metal_in
        self.metal -= self.metal_out
        self.water += self.water_in
        self.water -= self.water_out
        self.wood += self.wood_in
        print(f"Energy levels - Wood: {self.wood}, Fire: {self.fire}, Earth: {self.earth}, Metal: {self.metal}, Water: {self.water}")

    # 社交行为
    def greet(self, other_person):
        print(f"{self.name} says: Hello, {other_person.name}!")

    def make_friend(self, other_person):
        print(f"{self.name} and {other_person.name} are now friends.")

    # 消费行为
    def shop(self, item, amount):
        print(f"{self.name} bought {amount} of {item}.")

    def dine_out(self, restaurant):
        print(f"{self.name} is dining out at {restaurant}.")

    # 运动行为
    def exercise(self, activity, duration):
        print(f"{self.name} is doing {activity} for {duration} minutes.")

    def walk(self, distance):
        print(f"{self.name} walked {distance} kilometers.")

    # 为了填饱肚子的行为
    def eat(self, food, amount):
        print(f"{self.name} is eating {amount} of {food}.")

    def cook(self, dish):
        print(f"{self.name} is cooking {dish}.")

    def buy_groceries(self, grocery_list):
        print(f"{self.name} is buying the following groceries: {', '.join(grocery_list)}.")

    def speak(self, message, external_class):
        """
        Speak a given message and store it in the external class's global dictionary.

        Args:
            message (str): The message to speak.
            external_class (object): The external class instance that has a global dictionary.

        Returns:
            None
        """
        if hasattr(external_class, 'global_dict'):
            external_class.global_dict['message'] = message
            print(f"{self.name} says: {message}")
        else:
            print("The external class does not have a global dictionary.")

    def listen(self, external_class):
        """
        Listen to the external class's global dictionary and print the message if available.

        Args:
            external_class (object): The external class instance that has a global dictionary.

        Returns:
            None
        """
        if hasattr(external_class, 'global_dict') and 'message' in external_class.global_dict:
            message = external_class.global_dict['message']
            print(f"{self.name} heard: {message}")
        else:
            print("No message available in the external class's global dictionary.")

    # 环境影响
    def exposed_to_cold(self, temperature):
        print(f"{self.name} is exposed to a temperature of {temperature} degrees.")
        if temperature < 0:
            risk = 0.5  # 50% chance to catch a cold
        elif 0 <= temperature <= 10:
            risk = 0.2  # 20% chance to catch a cold
        else:
            risk = 0.05  # 5% chance to catch a cold

        if random.random() < risk:
            print(f"{self.name} caught a cold!")
        else:
            print(f"{self.name} is feeling fine.")

    # 遇到橘子
    def encounter_orange(self):
        print(f"{self.name} sees an orange.")
        decision = random.choice([True, False])  # 50% 概率去转动橘子
        if decision:
            self.turn_orange()
        else:
            print(f"{self.name} decides not to turn the orange.")

    def turn_orange(self):
        print(f"{self.name} is turning the orange with both hands.")

# 示例用法
#person1 = Person("Alice", 30, "Female")

# 遇到橘子
#person1.encounter_orange()
