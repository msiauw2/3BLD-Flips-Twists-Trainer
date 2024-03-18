#%% PROGRAM

# IMPORTS, FUNCTIONS, INITIAL VARIABLES
import kociemba
import random
from copy import deepcopy

# invert scramble

def invert_scramble(scr):
    # split scram into moves
    scr = scr.split()
    # iterate through moves
    for i in range(len(scr)):
        # if move has length 1 (e.g. R, U, F), then add a prime
        if len(scr[i]) == 1:
            scr[i] += "'"
        # if move has length 2 AND it's a prime move, remove the prime
        elif len(scr[i]) == 2:
            if scr[i][-1] == "'":
                scr[i] = scr[i][:-1]
                
    # finally, reverse the order of the moves
    scr.reverse()
    
    return ' '.join(scr)


# indices of all 12 edges in a cubestring
edge_indices = {'UB': [1,46], 'UR': [5,10], 'UF': [7,19], 'UL': [3,37],
                'FL': [21,41], 'FR': [23,12], 'BR': [48,14], 'BL': [50,39],
                'DF': [28,25], 'DR': [32,16], 'DB': [34,52], 'DL': [30,43]}

def edge_flip(cubestring,edge):
    """
    Parameters
    ----------
    cubestring : str
        string of 54 characters denoting current cube state
    edge : str
        name of edge piece, e.g. UF
    Returns
    -------
    str
        cubestring after edge flip
    """
    
    edge = edge_indices[edge]
    cubestring = list(cubestring)
    cubestring[edge[0]], cubestring[edge[1]] = cubestring[edge[1]], cubestring[edge[0]]
    return ''.join(cubestring)

# indices of all 12 corners in a cubestring
corner_indices = {'UBL': [0,47,36], 'UBR': [2,45,11], 'UFR': [8,20,9], 'UFL': [6,18,38],
                  'DBL': [33,53,42], 'DBR': [35,51,17], 'DFR': [29,26,15], 'DFL': [27,24,44]}

def corner_twist(cubestring,corner,direction):
    """
    Parameters
    ----------
    cubestring : STR
        string of 54 characters denoting current cube state
    corner : str
        name of edge piece, e.g. UFR
    direction : str
        either 'cw' or 'ccw' - direction of corner twist

    Returns
    -------
    str
        cubestring after corner twist

    """
    corner = corner_indices[corner]
    cubestring = list(cubestring)
    if direction == 'cw':
        if list(corner_indices.keys())[list(corner_indices.values()).index(corner)] in ['UBL','UFR','DBR','DFL']:
            cubestring[corner[0]], cubestring[corner[1]], cubestring[corner[2]] = cubestring[corner[1]], cubestring[corner[2]], cubestring[corner[0]]
        else:
            cubestring[corner[0]], cubestring[corner[1]], cubestring[corner[2]] = cubestring[corner[2]], cubestring[corner[0]], cubestring[corner[1]]
    elif direction == 'ccw':
        if list(corner_indices.keys())[list(corner_indices.values()).index(corner)] in ['UBL','UFR','DBR','DFL']:
            cubestring[corner[0]], cubestring[corner[1]], cubestring[corner[2]] = cubestring[corner[2]], cubestring[corner[0]], cubestring[corner[1]]
        else:
            cubestring[corner[0]], cubestring[corner[1]], cubestring[corner[2]] = cubestring[corner[1]], cubestring[corner[2]], cubestring[corner[0]]

    return ''.join(cubestring)

# the characters needed to insert a given edge piece (e.g. white-green = UF) into the cubestring
# each value of dict has multiple entries to allow for randomization of how an edge piece is inserted into cubestring/random state
edge_chars = {'UB': [['U', 'B'], ['B', 'U']], 'UR': [['U', 'R'], ['R', 'U']], 'UF': [['U', 'F'], ['F', 'U']], 'UL': [['U', 'L'], ['L', 'U']],
              'FL': [['F', 'L'], ['L', 'F']], 'FR': [['F', 'R'], ['R', 'F']], 'BR': [['B', 'R'], ['R', 'B']], 'BL': [['B', 'L'], ['L', 'B']],
              'DF': [['D', 'F'], ['F', 'D']], 'DR': [['D', 'R'], ['R', 'D']], 'DB': [['D', 'B'], ['B', 'D']], 'DL': [['D', 'L'], ['L', 'D']]}

# the characters needed to insert a given corner piece (e.g. white-green-red = UFR) into the cubestring
# each value has two sub lists. For example, under key 'UBL', the first list of the value
# is the possible arrangements of the corner when it's in UBL,UFR,DFL,DBR
# the second list of the value is possible arrangements of the corner in UBR,UFL,DFR,DBL
corner_chars = {
    'UBL': [
        [['U', 'B', 'L'], ['L', 'U', 'B'], ['B', 'L', 'U']],
        [['U', 'L', 'B'], ['B', 'U', 'L'], ['L', 'B', 'U']]
    ],
    'UBR': [
        [['U', 'B', 'R'], ['R', 'U', 'B'], ['B', 'R', 'U']],
        [['U', 'R', 'B'], ['B', 'U', 'R'], ['R', 'B', 'U']]
    ],
    'UFR': [
        [['U', 'F', 'R'], ['R', 'U', 'F'], ['F', 'R', 'U']],
        [['U', 'R', 'F'], ['F', 'U', 'R'], ['R', 'F', 'U']]
    ],
    'UFL': [
        [['U', 'F', 'L'], ['L', 'U', 'F'], ['F', 'L', 'U']],
        [['U', 'L', 'F'], ['F', 'U', 'L'], ['L', 'F', 'U']]
    ],
    'DBL': [
        [['D', 'B', 'L'], ['L', 'D', 'B'], ['B', 'L', 'D']],
        [['D', 'L', 'B'], ['B', 'D', 'L'], ['L', 'B', 'D']]
    ],
    'DBR': [
        [['D', 'B', 'R'], ['R', 'D', 'B'], ['B', 'R', 'D']],
        [['D', 'R', 'B'], ['B', 'D', 'R'], ['R', 'B', 'D']]
    ],
    'DFR': [
        [['D', 'F', 'R'], ['R', 'D', 'F'], ['F', 'R', 'D']],
        [['D', 'R', 'F'], ['F', 'D', 'R'], ['R', 'F', 'D']]
    ],
    'DFL': [
        [['D', 'F', 'L'], ['L', 'D', 'F'], ['F', 'L', 'D']],
        [['D', 'L', 'F'], ['F', 'D', 'L'], ['L', 'F', 'D']]
    ]
}

def random_state_scramble(cubestring, flips, twists):
    """
    Parameters
    ----------
    cubestring : str
        string of 54 characters denoting current cube state
    flips : int or str
        if int, number of edge flips desired. if str, then 'random'
    twists : int or str
        see above
    Returns
    -------
    str
        cubestring of random state scramble, with user-defined flips/twists

    """
    cubestring = list(cubestring)
    
    # keep track of which edges have/haven't already been used
    edge_chars_unused = deepcopy(edge_chars)
    # exclude any flipped edges from being affected by random state scramble
    for flip in edges_to_flip:
        del edge_chars_unused[flip]
    
    edge_indices_unused = deepcopy(edge_indices)
    for flip in edges_to_flip:
        del edge_indices_unused[flip]
    
    # iterate through each edge slot UB, UR, UF, etc.
    for edge_slot in edge_indices_unused:
        # get list of indices of edge slot
        edge_slot_indices = edge_indices_unused[edge_slot]
        # pick a random edge to put in edge_slot
        edge = random.choice(list(edge_chars_unused.keys()))
        # pick the permutation of the edge to insert (e.g. insert blue red vs red blue into UB)
        edge_colors = random.choice(edge_chars_unused[edge])
        
        if type(flips) == int:
            # if the edge we picked is the same as the slot it's going to, 
            # ensure it's going in solved instead of flipped (bc user already predefined flips)
            if edge == edge_slot:
                cubestring[edge_slot_indices[0]], cubestring[edge_slot_indices[1]] = edge_chars[edge][0][0], edge_chars[edge][0][1]
            # otherwise put the edge in a random permutation given by the randomly selected edge_colors
            else:
                cubestring[edge_slot_indices[0]], cubestring[edge_slot_indices[1]] = edge_colors[0], edge_colors[1]
        else:
            # if user selected 'random' number of edge flips, then just generate a random permutation of edges in the scramble
            cubestring[edge_slot_indices[0]], cubestring[edge_slot_indices[1]] = edge_colors[0], edge_colors[1]
            
        del edge_chars_unused[edge]
    
    # do the same process as above except for corners
    corner_chars_unused = deepcopy(corner_chars)
    for twist in corners_to_twist:
        del corner_chars_unused[twist]
        
    corner_indices_unused = deepcopy(corner_indices)
    for twist in corners_to_twist:
        del corner_indices_unused[twist]
    corners_group_1 = ['UBL','UFR','DBR','DFL']
    corners_group_2 = ['UBR','UFL','DBL','DFR']
    
    for corner_slot in corner_indices_unused:
        corner_slot_indices = corner_indices_unused[corner_slot]
        corner = random.choice(list(corner_chars_unused.keys()))
        if (corner_slot in corners_group_1 and corner in corners_group_1) or (corner_slot in corners_group_2 and corner in corners_group_2):
            corner_colors = random.choice(corner_chars[corner][0])
        else:
            corner_colors = random.choice(corner_chars[corner][1])
        
        
        if type(twists) == int:
            # if the edge we picked is the same as the slot it's going to, 
            # ensure it's going in solved instead of flipped (bc user already predefined flips)
            if corner == corner_slot:
                cubestring[corner_slot_indices[0]], cubestring[corner_slot_indices[1]], cubestring[corner_slot_indices[2]] = corner_chars[corner][0][0][0], corner_chars[corner][0][0][1], corner_chars[corner][0][0][2]  
            else:
                cubestring[corner_slot_indices[0]], cubestring[corner_slot_indices[1]], cubestring[corner_slot_indices[2]] = corner_colors[0], corner_colors[1], corner_colors[2]
        else:
            # if user selected 'random' number of corner twists, then just generate a random permutation of corners in the scramble
            cubestring[corner_slot_indices[0]], cubestring[corner_slot_indices[1]], cubestring[corner_slot_indices[2]] = corner_colors[0], corner_colors[1], corner_colors[2]
        del corner_chars_unused[corner]
    
    cubestring = fix_corner_twist(cubestring,corner_buffer) 
    cubestring = fix_edge_flip(cubestring, edge_buffer) 
    cubestring = fix_parity(cubestring, edge_buffer) 
    
    return ''.join(cubestring)

# fix corner twist problem by twisting the buffer, if necessary
def fix_corner_twist(cubestring, buffer):
    """
    Parameters
    ----------
    cubestring : str
        string of 54 characters denoting current cube state
    buffer : str
        corner buffer, e.g. 'UFR' or 'UBL'
    Returns
    -------
    str
        cubestring with corner twist problem fixed (via twisting buffer)
    """
    cubestring = list(cubestring)
    
    # at the end of this function, this variable will be divided by 3 and the remainder kept
    # 0 = no corner twist issue, 1 = must twist buffer ccw, 2 = must twist buffer cw
    total_twist_state = 0
    
    # depending on which corner slot a corner is going into, that dictates which
    # of the two nested lists to use from corner_chars
    corners_group_1 = ['UBL','UFR','DBR','DFL']
    corners_group_2 = ['UBR','UFL','DBL','DFR'] 
    
    # iterate through eight corners
    for corner in corner_indices.values():
        # get colors of the corner in the slot - e.g. a white-green-red corner in UBL
        # is simply 'UFR'
        corner_colors = list(cubestring[corner[0]]+cubestring[corner[1]]+cubestring[corner[2]])
        # get current corner SLOT - 'UBL', 'UBR', etc
        corner_name = list(corner_indices.keys())[list(corner_indices.values()).index(corner)]
        
        if corner_name in corners_group_1:
            try:
                twist_value = corner_colors.index('U')
            except:
                twist_value = corner_colors.index('D')
            if twist_value == 0:
                pass
            elif twist_value == 1:
                twist_value = 2
            elif twist_value == 2:
                twist_value = 1
        elif corner_name in corners_group_2:
            try:
                twist_value = corner_colors.index('U')
            except:
                twist_value = corner_colors.index('D')
        total_twist_state += twist_value
    
    total_twist_state = total_twist_state % 3

    if total_twist_state == 0:
        # no twist needed
        pass
    elif total_twist_state == 1:
        # twist buffer ccw
        cubestring = corner_twist(''.join(cubestring), buffer, 'ccw')
    elif total_twist_state == 2:
        # twist buffer cw
        cubestring = corner_twist(''.join(cubestring), buffer, 'cw')

    return ''.join(cubestring)

# fix edge flip parity problem by flipping the buffer, if necessary
def fix_edge_flip(cubestring, buffer):
    """
    Parameters
    ----------
    cubestring : str
        string of 54 characters denoting current cube state
    buffer : str
        edge buffer, e.g. 'UF' or 'UB'
    Returns
    -------
    str
        cubestring after edge flip problem fixed (via flipping buffer)
    """
    cubestring = list(cubestring)
    
    oriented_edges = 0
    
    # iterate through edges
    for indices in edge_indices.values():
        UFBD_sticker = cubestring[indices[0]]
        RL_sticker = cubestring[indices[1]]
        # if U/F/B/D sticker of edge (first index of each edge_indices pair) is white/yellow it's a good edge
        if UFBD_sticker == 'U' or UFBD_sticker == 'D':
            oriented_edges += 1
        # else, if U/F/B/D sticker is green/blue AND it's an F2L edge, then it's good
        elif UFBD_sticker == 'F' or UFBD_sticker == 'B':
            if RL_sticker != 'U' and RL_sticker != 'D':
                oriented_edges += 1
    
    edge_parity = oriented_edges % 2  
    if edge_parity == 1:
        cubestring = edge_flip(''.join(cubestring), buffer)
    
    return ''.join(cubestring)

# fix parity problem by swapping buffer with a random edge (not one that's been flipped)
def fix_parity(cubestring, buffer):
    """
    Parameters
    ----------
    cubestring : str
        string of 54 characters denoting current cube state.
    buffer : str
        edge buffer, e.g. 'UF' or 'UB'
    Returns
    -------
    str
        cubestring after parity problem fixed (via swapping buffer w/ non-flipped edge)

    """
    cubestring = list(cubestring)
    
    # if kociemba recognizes the scramble as a valid state, then done
    try:
        kociemba.solve(''.join(cubestring))
    # if kociemba doesn't recognize the scramble as a valid state, swap the buffer with another edge
    except:
        # keep track of which edges not flipped yet - buffer excluded bc we're always going to switch the buffer w/ smth    
        edges_not_flipped = ['UB','UR','UF','UL','FL','FR','BL','BR','DF','DR','DB','DL'] 
        edges_not_flipped.remove(buffer)
        for flip in edges_to_flip:
            edges_not_flipped.remove(flip)
        buffer_indices = edge_indices[buffer]
        swap_edge = random.choice(edges_not_flipped)
        swap_edge_indices = edge_indices[swap_edge]
        
        # swap buffer with swap edge
        cubestring[buffer_indices[0]], cubestring[buffer_indices[1]], cubestring[swap_edge_indices[0]], cubestring[swap_edge_indices[1]] = cubestring[swap_edge_indices[0]], cubestring[swap_edge_indices[1]], cubestring[buffer_indices[0]], cubestring[buffer_indices[1]]
    
    return ''.join(cubestring)

#%% FLASK

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gen_scramble', methods=['POST'])
def gen_scramble():
    data = request.get_json()
    
    # get user-inputted variables
    global edge_buffer
    edge_buffer = data['edgeBuffer']
    global corner_buffer
    corner_buffer = data['cornerBuffer']
    
    try:
        flips = int(data['edgeFlips'])
    except:
        flips = 'random'
        
    try:
        twists = int(data['cornerTwists'])
    except:
        twists = 'random'
        
    # generate scramble
    
    solved = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
    # this WILL be the cubestring of our random state scramble with flips + twists
    scr_string = solved

    # flip edges
    edges_excl_buffer = list(edge_indices.keys())
    edges_excl_buffer.remove(edge_buffer)
    
    # randomly selected edge(s) to flip - number of edges assigned by user
    # if user selected 'Random' flips, then don't "pre-flip" any edges
    global edges_to_flip
    if type(flips) == int:    
        edges_to_flip = random.sample(edges_excl_buffer,flips)
        for i in range(flips):
            scr_string = edge_flip(scr_string, edges_to_flip[i])
    else:
        edges_to_flip = []
    
        
    # twist corners
    corners_excl_buffer = list(corner_indices.keys())
    corners_excl_buffer.remove(corner_buffer)
    # if user selected 'Random' twists, then don't "pre-twist" any corners
    global corners_to_twist
    if type(twists) == int:
        corners_to_twist = random.sample(corners_excl_buffer,twists)
        for i in range(twists):
            scr_string = corner_twist(scr_string, corners_to_twist[i], random.choice(['cw','ccw']))
    else:
        corners_to_twist = []
    
        
    # generate scramble
    # cubestring of random state scramble after flips/twists
    scr_string = random_state_scramble(scr_string, flips, twists)
    # solution to random state scramble
    solution = kociemba.solve(scr_string)
    # inverse to solution IS the random state scramble
    scr = invert_scramble(solution)

    return jsonify({'result': scr})

@app.route('/gen_mult_scrambles', methods=['POST'])
def gen_mult_scrambles():
    data = request.get_json()
    edgeFlipOptions = data['edgeFlipOptions']
    cornerTwistOptions = data['cornerTwistOptions']
    numScrams = data['numScrams']
    scrams = [""] * numScrams
    
    # get user-inputted variables
    global edge_buffer
    edge_buffer = data['edgeBuffer']
    global corner_buffer
    corner_buffer = data['cornerBuffer']
    
    for j in range(numScrams):
        flips = random.choice(edgeFlipOptions)
        try:
            flips = int(flips)
        except:
            flips = 'random'
            
        twists = random.choice(cornerTwistOptions)
        try:
            twists = int(twists)
        except:
            twists = 'random'
            
        # generate scramble
        
        solved = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
        # this WILL be the cubestring of our random state scramble with flips + twists
        scr_string = solved
    
        # flip edges
        edges_excl_buffer = list(edge_indices.keys())
        edges_excl_buffer.remove(edge_buffer)
        
        # randomly selected edge(s) to flip - number of edges assigned by user
        # if user selected 'Random' flips, then don't "pre-flip" any edges
        global edges_to_flip
        if type(flips) == int:    
            edges_to_flip = random.sample(edges_excl_buffer,flips)
            for i in range(flips):
                scr_string = edge_flip(scr_string, edges_to_flip[i])
        else:
            edges_to_flip = []
        
            
        # twist corners
        corners_excl_buffer = list(corner_indices.keys())
        corners_excl_buffer.remove(corner_buffer)
        # if user selected 'Random' twists, then don't "pre-twist" any corners
        global corners_to_twist
        if type(twists) == int:
            corners_to_twist = random.sample(corners_excl_buffer,twists)
            for i in range(twists):
                scr_string = corner_twist(scr_string, corners_to_twist[i], random.choice(['cw','ccw']))
        else:
            corners_to_twist = []
        
            
        # generate scramble
        # cubestring of random state scramble after flips/twists
        scr_string = random_state_scramble(scr_string, flips, twists)
        # solution to random state scramble
        solution = kociemba.solve(scr_string)
        # inverse to solution IS the random state scramble
        scr = invert_scramble(solution)
        
        scrams[j] = scr
    
    return jsonify({'result': scrams})

if __name__ == '__main__':
    app.run(debug=True)
