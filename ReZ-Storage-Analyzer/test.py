import keyboard
import random

a = ["ananas", "arbuz", "agrest"]
b = ["banan", "balon", "beton"]
c = ["cytryna", "cebula", "candy"]
# ...

while True: 
    try:  
        if keyboard.is_pressed('a'):
            print(random.choice(a))
            break
        elif keyboard.is_pressed('b'):
            print(random.choice(b))
            break
        elif keyboard.is_pressed('c'):
            print(random.choice(c))
            break
        # implement more elif here
    except:
        break 

