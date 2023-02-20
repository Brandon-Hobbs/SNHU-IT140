#Brandon HObbs
#6-6-2021


#global variables
inventory_list = []

#room container that holds all of the items and connectors between rooms
room_container = {
        'Great Hall': {'south': 'Bedroom', 'item': 'Item A'},
        'Bedroom': {'north': 'Great Hall', 'east': 'Cellar', 'item': 'Item B'},
        'Cellar': {'west': 'Bedroom', 'item': 'Item C'}
    }

#     {
#     'Foyer': {'east': 'Great Hall', 'item': None},
#     'Great Hall': {'north': 'Antechamber', 'south': 'Library', 'east': 'Kitchen', 'west': 'Foyer', 'item': 'Nice Hat'},
#     'Antechamber': {'south': 'Great Hall', 'east': "Queen's Chamber",'item': "Trusty Stallion"},
#     "Queen's Chamber": {'west': 'Antechamber', 'item': None},
#     'Library': {'north': 'Great Hall', 'east': 'Study','item': "Magic Scepter"},
#     'Study': {'west': 'Library', 'item': 'Gardening Shears'},
#     'Kitchen': {'north': 'Larder','west': 'Great Hall', 'item': 'Magic Spell'},
#     'Larder': {'south': 'Kitchen','item': 'Imp Named Bob'}
# }



def print_manager(event):
    #function adds a master repo for printable text

    messages = {
        'welcome': "The Princess has been separated from her Prince but can hear him somewhere in the creepy mansion.\n"
                   "Worryingly, however, she can also hear a strange cackling coming from deep within...\n"
                   "Stories precede the mansion, however, and the Princess knows the Queen of Octopuses lives there.\n"
                   "Maybe if the Princess can find everything needed to scare the Queen her Prince will be found safe…\n",
        'item_not_picked_up': 'There is an item in the room you have not picked up.\n',
        'item_warn': "Item not found.\n",
        'item_success': "Item added to your inventory successfully.\n",
        'room_move': 'Moved to the new room successfully.\n',
        'room_warn': "There is no room in that direction.\n",
        "boss_fight": "Boss rules.\n",
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

if __name__ == '__main__':

    #let's welcome the player and give them the rules
    print_manager('welcome')
    print_manager('rules')

    #variable init
    user_command = ''
    move_direction = ''
    current_room = 'Bedroom'
    room_item = ''

    #main loop
    while user_command != 'quit':

        user_command = input('Please enter a command:').lower().strip()

        if user_command == 'move':
            move_direction = input('Please select a direction to travel:').lower().strip()
            current_room, room_item = move_room(move_direction, current_room)

            #check if the room item is in inventory warn that it's still available
            if room_item not in inventory_list and room_item != None:
                print_manager('item_not_picked_up')

        elif user_command == 'get':
            if get_item(room_item, current_room):
                print_manager('item_success')
            else:
                print_manager('item_warn')

        elif user_command == 'rules':
            print_manager('rules')

        #let's be helpful and show the inventory
        elif user_command == 'inventory':
            if len(inventory_list) == 0: #handle the null inventory
                print('Inventory is empty.')
            else:
                print(*inventory_list, sep=', ')

        elif user_command == 'map':
            room_print(current_room)

        elif user_command == 'quit':
            break

        else:
            continue #Do nothing for now





