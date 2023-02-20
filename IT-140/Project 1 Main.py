#global variables
inventory_list = []

room_container = {
    'Foyer': {'east': 'Great Hall', 'item': None},
    'Great Hall': {'north': 'Antechamber', 'south': 'Library', 'east': 'Kitchen', 'west': 'Foyer', 'item': 'Nice Hat'},
    'Antechamber': {'south': 'Great Hall', 'east': "Queen's Chamber",'item': "Trusty Stallion"},
    "Queen's Chamber": {'west': 'Antechamber', 'item': None},
    'Library': {'north': 'Great Hall', 'east': 'Study','item': "Magic Scepter"},
    'Study': {'west': 'Library', 'item': 'Gardening Shears'},
    'Kitchen': {'north': 'Larder','west': 'Great Hall', 'item': 'Magic Spell'},
    'Larder': {'south': 'Kitchen','item': 'Imp Named Bob'}
}

item_power ={
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
        'boss_rules': "To use an item type 'use' and then select the item by name.\n"
                      "To display your current inventory type 'inventory'.\n"
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
                 "To display your current inventory type 'inventory'.\n"
                 "To display your current location type 'map'.\n"
                 "To quit the game type 'quit'.\n"
                 "To review the commands type 'rules' at the prompt.\n"
    }

    print(messages[event])


def get_item(item, current_room):
    #need to get the item in the current room ->decide if that item is available or not, and then pick it up if requested
    #Warn if trying to get an item that is already picked up or not available
    if item == None:
        return False
    elif item == room_container[current_room]['item'] and item not in inventory_list:
        inventory_list.append(item)
        return  True
    elif item == room_container[current_room]['item'] and item in inventory_list: #Item already picked up
        return  False
    elif item != room_container[current_room]['item']: #item not even in room
        return False
    else: #unknown error/state
        return False

def use_item(item):
    #lets be nice and prtect again capitalization issues
    tmp_list = [x.lower() for x in inventory_list]

    if item == None: #small error handling
        return False
    elif item in tmp_list: #let's consume the item
        inventory_list.remove(item.title())
        print_manager('item_used')
        return True
    elif item not in tmp_list:
        print_manager('item_used_warn')
        return False

def move_room(move, current_room):
    #need to help naviagte the map
    #return room, item
    if move in room_container[current_room].keys():
        print_manager('room_move')
        room_print(room_container[current_room][move])
        return room_container[current_room][move], room_container.get(room_container[current_room][move])['item']
    else:
        print_manager('room_warn')
        room_print(current_room)
        return current_room, room_container[current_room]['item']

def room_print(current_room):
    #print the current room. Lets do this as a function so we can use everywhere
    print('Currently, you are in the {}'.format(current_room))
    print()

def boss_fight():
    #this is the boss fight sequence
    #boss and player both start at a life of 100
    #If the user uses an item and it is in their inventory boss --
    #if the user uses an item and it is NOT in their inventory user --
    #first to zero losses
    print_manager('boss_fight')
    print_manager('boss_rules')

    #variable init
    user_command = ''
    user_life = 100
    boss_life = 100

    # global inventory_list
    # inventory_list = ['Trusty Stallion', 'Nice Hat', 'Magic Scepter']

    while user_command != 'flee' and user_life > 0 and boss_life > 0:
        print("Fight Status: User Life {} vs Queen Life {}".format(user_life, boss_life))
        print()
        user_command = input('Please enter a command:').lower().strip()
        print()
        if user_command == 'flee':
            move_room('west', "Queen's Chamber")
            break

        elif user_command == 'inventory':
            if len(inventory_list) == 0: #handle the empty list
                print('Inventory is empty.')
            else:
                print(*inventory_list, sep=', ')
            print()

        elif user_command == 'use':
            print_manager('boss_items')
            print(*item_power.keys(), sep=', ')
            print()
            item_used = input('What item do you want to use:').strip().lower()

            if use_item(item_used): #this means the item was deployed ok
                boss_life -= item_power.get(item_used.title(), 0)

            else:
                user_life -= item_power.get(item_used.title(), 0)

        else:
            continue
            #do nothing for now

    else:#else for the while
        if user_life <= 0:
            print_manager('user_dead')
            return True
        elif boss_life <= 0:
            print_manager('boss_dead')
            return True


if __name__ == '__main__':

    #let's welcome the player and give them the rules
    print_manager('welcome')
    print_manager('rules')

    #variable init
    user_command = ''
    move_direction = ''
    current_room = 'Foyer'
    room_item = ''
    game_over = False

    #main loop
    while user_command != 'quit' and not game_over:

        user_command = input('Please enter a command:').lower().strip()
        print()

        if user_command == 'move':
            move_direction = input('Please select a direction to travel:').lower().strip()
            current_room, room_item = move_room(move_direction, current_room)

            #check if the room item is in inventory warn that it's still available
            if room_item not in inventory_list and room_item != None:
                print_manager('item_not_picked_up')

            #throw a boss fight warning when one room away
            if current_room == 'Antechamber':
                print_manager('boss_warn')
            #Start the fight if you go into the queen's chamber
            elif current_room == "Queen's Chamber":
                game_over = boss_fight()

                if not game_over: #if user flee need to reset the current room
                    current_room = 'Antechamber'

        elif user_command == 'get':
            if get_item(room_item, current_room):
                print_manager('item_success')
            else:
                print_manager('item_warn')

        elif user_command == 'rules':
            print_manager('rules')

        elif user_command == 'inventory':
            if len(inventory_list) == 0: #handle the empty list
                print('Inventory is empty.')
            else:
                print(*inventory_list, sep=', ')

            print()

        elif user_command == 'quit':
            break

        elif user_command == 'map':
            room_print(current_room)

        else:
            continue
            #Do nothing for now




