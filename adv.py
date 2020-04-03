from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

opposites = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

def find_paths(first_room, visited=set()):
    cur_visited = set()
    for room in visited: 
        cur_visited.add(room)
    path = []
    def add_to_path(room, back=None):
        cur_visited.add(room)
        exits = room.get_exits()
        for direction in exits:
            if room.get_room_in_direction(direction) not in cur_visited:
                path.append(direction)
                add_to_path(room.get_room_in_direction(direction), opposites[direction])
        if back: 
            path.append(back)
    add_to_path(first_room)
    return path

def shortest_path(first_room, visited=set()):
    path = []
    def add_to_path(room, back=None):
        visited.add(room)
        exits = room.get_exits()
        path_lengths = {}
        for direction in exits:
            path_lengths[direction] = len(find_paths(room.get_room_in_direction(direction), visited))
        traverse_order = []
        sorted_paths = sorted(path_lengths.items(), key=lambda x: x[1])
        for key, _ in sorted_paths: 
            traverse_order.append(key)
        for direction in traverse_order:
            if room.get_room_in_direction(direction) not in visited:
                path.append(direction)
                add_to_path(room.get_room_in_direction(direction), opposites[direction])
        if len(visited) == len(world.rooms): 
            return
        elif back: 
            path.append(back)
    add_to_path(first_room)
    return path

traversal_path = shortest_path(world.starting_room)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
