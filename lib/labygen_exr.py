##--Dydy2412--##
from random import shuffle, randint

def get_all_dir(cell_x_dir, cell_y_dir):
    '''retourne toutes les directions possibles que peu prendre la tête'''
    return [(cell_x_dir+i,cell_y_dir+j) for i in range(-1,2) for j in range(-1,2) if bool(i == 0) != bool(j == 0)]

def get_inside_dir(directions_ins, L_ins, l_ins):
    '''retire les direction en dehor du labyrynther des directions possibles'''
    return [directions_ins[i] for i in range(len(directions_ins)) if 0 <= directions_ins[i][0] < L_ins and 0 <= directions_ins[i][1] < l_ins]

def get_aviable_dir(aviable_dir, cells_dir, cell_x_aviable, cell_y_aviable, id):
    ''''retire les directions déja emprunters au direction possible'''
    return [aviable_dir[i] for i in range(len(aviable_dir)) if cells_dir[aviable_dir[i][0]][aviable_dir[i][1]] != id]

def get_breakable_walls(cell_x_break, cell_y_break, cells, L_break, l_break, id):
    '''retoune les seul positon que peu prendre la tête'''
    return get_aviable_dir(get_inside_dir(get_all_dir(cell_x_break, cell_y_break), L_break, l_break), cells, cell_x_break, cell_y_break, id)

def shuffled(li):
    '''retourne la liste mélanger sous forme de valeur'''
    shuffle(li)
    return li

def get_wall_coord(x_, y_, x_dest, y_dest):
    '''retourne les cordonnées du mur impliqué dans le direction d expension'''
    if x_dest == x_:
        if y_dest < y_:
            return (0,(x_,y_))
        else:
            return (0,(x_dest, y_dest))
    elif y_dest == y_:
        if x_dest < x_:
            return (1,(x_,y_))
        else:
            return (1,(x_dest,y_dest))

def discover_cells(x_start, y_start, vwall_ex, hwall_ex, cells_ex, L_ex, l_ex, id):
    '''dévoile un cellule puis regarde ou s étendre'''

    dir_aviable = shuffled(get_breakable_walls(x_start, y_start, cells_ex, L_ex, l_ex, id))
    
    cells_ex[x_start][y_start] = id

    for direct in dir_aviable:
        if direct in get_breakable_walls(x_start, y_start, cells_ex, L_ex, l_ex, id):
            x = direct[0]
            y = direct[1]

            walls = get_wall_coord(x_start, y_start, x, y)
            walls_x = walls[1][0]
            walls_y = walls[1][1]

            if walls[0] == 0:
                vwall_ex[walls_x][walls_y] = True
            else:
                hwall_ex[walls_x][walls_y] = True
            
            discover_cells(x, y, vwall_ex, hwall_ex, cells_ex, L_ex, l_ex, id)

def gen_laby_ex(vwall_ex, hwall_ex, cells_ex, L_ex, l_ex, is_path):
    '''initialise la recursion'''
    x_start = randint(0, L_ex-1)
    y_start = randint(0, l_ex-1)
    id = 'O'

    discover_cells(x_start, y_start,vwall_ex, hwall_ex, cells_ex, L_ex, l_ex, id)

    #ajout d une entré et d'une sortie
    if is_path:
        vwall_ex[0][0] = True
        vwall_ex[L_ex-1][l_ex] = True
    
    return cells_ex, vwall_ex, hwall_ex