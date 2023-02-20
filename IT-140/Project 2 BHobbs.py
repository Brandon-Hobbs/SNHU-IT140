#project 2
#Brandon Hobbs

import os

#global variables
inventory_list = []
used_inventory = []

class PlayerLife:  # just to keep track of the players' life

    def __init__(self):
        self.princess = 100
        self.boss = 100

room_container = {
    'Foyer': {'east': 'Great Hall', 'item': None},
    'Great Hall': {'north': 'Antechamber', 'south': 'Library', 'east': 'Kitchen', 'west': 'Foyer', 'item': 'Nice Hat'},
    'Antechamber': {'south': 'Great Hall', 'east': "Queen's Chamber", 'item': "Trusty Stallion"},
    "Queen's Chamber": {'west': 'Antechamber', 'item': None},
    'Library': {'north': 'Great Hall', 'east': 'Study', 'item': "Magic Scepter"},
    'Study': {'west': 'Library', 'item': 'Gardening Shears'},
    'Kitchen': {'north': 'Larder', 'west': 'Great Hall', 'item': 'Magic Spell'},
    'Larder': {'south': 'Kitchen', 'item': 'Imp Named Bob'}
}

item_power = {
    'Nice Hat': 25,
    'Trusty Stallion': 10,
    'Magic Scepter': 15,
    'Gardening Shears': 6,
    'Magic Spell': 33,
    'Imp Named Bob': 11
}

def print_manager(event):
    # function adds a master repo for printable text
    messages = {
        'welcome': "The Princess has been separated from her Prince but can hear him somewhere in the creepy mansion.\n"
                   "Worryingly, however, she can also hear a strange cackling coming from deep within...\n"
                   "Stories precede the mansion, however, and the Princess knows the Queen of Octopuses lives there.\n"
                   "Maybe if the Princess can find everything needed to scare the Queen her Prince will be found safe...\n",
        'item_not_picked_up': 'There is an item in the room you have not picked up.\n',
        'item_warn': "Item not found.\n",
        'item_success': "Item added to your inventory successfully.\n",
        'room_move': 'Moved to the new room successfully.\n',
        'room_warn': "There is no room in that direction.\n",
        'boss_warn': "From behind a door in the room you hear the cackling again but so much louder...\n"
                     "The Queen of Octopuses must be beyond that door...\n"
                     "Maybe your Prince will be there as well...if it isn't too late.\n",
        'boss_fight': "The Queen of Octopuses sits upon her thrown as you burst into her chamber.\n"
                      "She rises on her eight grotesque feet and you catch a glimpse of your Prince.\n"
                      "Maybe the items you have collected will be of some use against the evil Queen...\n",
        'boss_rules': "To use an item type 'use' and then type the item by name.\n"
                      "To run away type 'flee'.\n",
        'boss_items': "The Queen is allergic to the following items, have you seen any of them...\n",
        'item_used': 'The item was deployed successfully. Take that you bit...\n',
        'item_used_warn': "Princess, that item was not found check the name and try again.\n",
        'user_dead': 'I am so sorry Princess but you have died. I hope the Prince will be happy here for the '
                     'rest of his life...\n',
        'boss_dead': 'Congratulations Princess you have defeated the Queen of the Octopuses.\n'
                     'Your Prince emerges a little worse for wear but even more in love than before.\n'
                     'Enjoy your lives together happily ever after.\n',
        'rules': "Please guide the Princess on her journey.\n"
                 "To move type 'move' and then select 'east', 'west', 'north', 'south'.\n"
                 "To pick up an item that is in the room type 'get'.\n"
                 "To quit the game type 'quit'.\n"
                 "To review the commands type 'rules' at the prompt.\n",
        'invalid_command': "Please enter a valid command. Type 'rules' if you need help.\n"
    }

    return messages[event]


def get_item(item, current_room):
    #need to get the item in the current room ->decide if that item is available or not, and then pick it up if requested
    #Warn if trying to get an item that is already picked up or not available
    if item is None:
        return False
    elif item == room_container[current_room]['item'] and item not in inventory_list:
        inventory_list.append(item)
        return True
    elif item == room_container[current_room]['item'] and item in inventory_list: #Item already picked up
        return False
    elif item != room_container[current_room]['item']:  #item not even in room
        return False
    else:  #unknown error/state
        return False

def use_item(item):
    #lets be nice and protect against capitalization issues
    tmp_list = [x.lower() for x in inventory_list]

    if item is None:  #small error handling
        return False
    elif item in tmp_list:  #let's consume the item
        used_inventory.append(item.title())
        inventory_list.remove(item.title())
        return True
    elif item not in tmp_list:
        return False

def move_room(move, current_room):
    #need to help navigate the map
    #return room, item, message
    if move in room_container[current_room].keys():
        return room_container[current_room][move], room_container.get(room_container[current_room][move])['item'], print_manager('room_move')
    else:
        return current_room, room_container[current_room]['item'], print_manager('room_warn')

def room_print(current_room):
    #print the current room. Lets do this as a function so we can use everywhere
    print('Currently, you are in the {}'.format(current_room))

def boss_fight():
    #this is the boss fight sequence
    #boss and player both start at a life of 100
    #If the user uses an item and it is in their inventory boss --
    #if the user uses an item and it is NOT in their inventory user --
    #first to zero losses

    #variable init
    user_command = ''

    current_message = print_manager('boss_fight') + '\n'
    current_message += print_manager('boss_rules')

    # global inventory_list
    # inventory_list = ['Trusty Stallion', 'Nice Hat', 'Magic Scepter']

    while user_command != 'flee' and player1.princess > 0 and player1.boss > 0:

        os.system('cls||echo -e \\\\033c')

        print('*' * 20)
        print()
        print("Fight Status: User Life {} vs Queen Life {}".format(player1.princess, player1.boss))
        print()
        print('Inventory:', end=' ')
        print(*inventory_list, sep=', ')
        print()
        print("Messages:\n" + current_message)
        print('*' * 20)

        current_message = ''  #clear the prompt

        user_command = input('Please enter a command:').lower().strip()
        print()

        if user_command == 'flee':
            move_room('west', "Queen's Chamber")
            break

        elif user_command == 'rules':
            current_message += print_manager('boss_rules')

        elif user_command == 'use':
            print(print_manager('boss_items'))
            print(*item_power.keys(), sep=', ')
            print()
            item_used = input('What item do you want to use:').strip().lower()

            if use_item(item_used):  #this means the item was deployed ok
                current_message += print_manager('item_used')

                player1.boss -= item_power.get(item_used.title(), 0)

            else:
                player1.princess -= 20  #user takes a hit

                current_message += print_manager('item_used_warn')

        else:
            current_message += print_manager('invalid_command')

    else:  #else for the while
        if player1.princess <= 0 or player1.boss <= 0:
            return True
        else:
            return False


if __name__ == '__main__':

    #variable init
    user_command = ''
    move_direction = ''
    current_room = 'Foyer'
    room_item = ''
    game_over = False

    #let's welcome the player and give them the rules
    current_message = print_manager('welcome') + '\n'
    current_message += print_manager('rules')

    player1 = PlayerLife()  #create the player

    #main loop
    while user_command != 'quit' and not game_over:

        os.system('cls||echo -e \\\\033c')

        #make a small user dashboard
        print('*' * 20)
        print()
        room_print(current_room)
        print()
        print('Inventory:', end=' ')
        print(*inventory_list, sep=', ')
        print()
        print('Messages:\n' + current_message)
        print('*' * 20)

        user_command = input('Please enter a command:').lower().strip()
        print()

        current_message = ''

        if user_command == 'move':
            move_direction = input('Please select a direction to travel:').lower().strip()
            current_room, room_item, current_message = move_room(move_direction, current_room)

            #check if the room item is in inventory warn that it's still available
            if room_item not in inventory_list and room_item not in used_inventory and room_item is not None:
                current_message += print_manager('item_not_picked_up')

            #throw a boss fight warning when one room away
            if current_room == 'Antechamber':
                current_message += print_manager('boss_warn')
            #Start the fight if you go into the queen's chamber
            elif current_room == "Queen's Chamber":
                game_over = boss_fight()

                if not game_over:  #if user flee need to reset the current room
                    current_room = 'Antechamber'

        elif user_command == 'get':
            if get_item(room_item, current_room):
                current_message += print_manager('item_success')
            else:
                current_message += print_manager('item_warn')

        elif user_command == 'rules':
            current_message += print_manager('rules')

        elif user_command == 'quit':
            break

        else:
            current_message += print_manager('invalid_command')

    # game over who's dead?
    if player1.princess <= 0:
        os.system('cls||echo -e \\\\033c')
        print(print_manager('user_dead'))
    elif player1.boss <= 0:
        os.system('cls||echo -e \\\\033c')
        print(print_manager('boss_dead'))

    #hold the terminal to say good bye
    user_command = input('Press any key to quit.')
