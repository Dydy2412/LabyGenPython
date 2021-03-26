##--Dydy2412--##
from random import shuffle

def is_pair(i):
    '''Test si un nombre est pair'''
    return i%2 == 0

def get_vert_interiror(matrix_v_int):
    '''retire les coté d une matrice'''
    return [[matrix_v_int[j][i] for i in range(len(matrix_v_int[j])) if 0 < i < len(matrix_v_int[j])-1] for j in range(len(matrix_v_int))]

def get_horiz_interiror(matrix_h_int):
    '''retire le dessus et le desous d 'une matrice'''
    return [[matrix_h_int[j][i] for i in range(len(matrix_h_int[j]))] for j in range(len(matrix_h_int)) if 0 < j < len(matrix_h_int)-1]

def get_false_count(matrix_f_count):
    '''retourne le nombre de False (de mur) dans une matrice booléene'''
    return [matrix_f_count[i][j] for i in range(len(matrix_f_count)) for j in range(len(matrix_f_count[i]))].count(False)

def get_wall_count(vwall_count, hwall_count):
    '''retourne le nombre de mur total dans le labyrinthe'''
    return get_false_count(vwall_count) + get_false_count(hwall_count)

def get_wall_coords(vwall_coord, hwall_coords):
    ''''retourne une loste de toute les coordonné des murs'''
    return [(0, (i,j)) for i in range(len(vwall_coord )) for j in range(len(vwall_coord[i]))] + [(1, (i,j)) for i in range(len(hwall_coords)) for j in range(len(hwall_coords[i]))]

def gen_steps(coords):
    '''melange l'ordre des mur'''
    shuffle(coords)
    return coords

def get_cell_wall(cell_x_c, cell_y_c):
    '''retourne les coordonné de mur au alentour de la cellule'''
    return { 'W' : (0, (cell_x_c, cell_y_c) ), 'N' : (1, (cell_x_c, cell_y_c) ), 'E' : (0, (cell_x_c, cell_y_c+1) ), 'S' : (1, (cell_x_c+1, cell_y_c) )}

def get_faced_wall(cell_x_f, cell_y_f, facing):
    '''retourne l orde deverification des murs suivant la directions'''
    cell_wall = get_cell_wall(cell_x_f, cell_y_f)
    
    if facing == 'north':
        return [cell_wall['W'], cell_wall['N'], cell_wall['E']] #WNE
    elif facing == 'south':
        return [cell_wall['E'], cell_wall['S'], cell_wall['W']] #ESW
    elif facing == 'east':
        return [cell_wall['N'], cell_wall['E'], cell_wall['S']] #NES
    elif facing == 'west':
        return [cell_wall['S'], cell_wall['W'], cell_wall['N']] #SWN
    else:
        return None

def id_propagation(vwall_id, hwall_id, cells_id, steps_id, cell_x_id, cell_y_id, id, facing_id):
    '''Propage l id de la cellule vers les autres pour unifier le chemin'''
    cell_wall = get_faced_wall(cell_x_id, cell_y_id, facing_id)
    cells_id[cell_x_id][cell_y_id] = id

    for wall in cell_wall:
        wall_d = wall[0]
        wall_x = wall[1][0]
        wall_y = wall[1][1]

        if wall_d == 0:
            
            if vwall_id[wall_x][wall_y]:
                if (wall_x == cell_x_id and wall_y == cell_y_id):
                    id_propagation(vwall_id, hwall_id, cells_id, steps_id, cell_x_id, cell_y_id-1, id, 'west')
                else:
                    id_propagation(vwall_id, hwall_id, cells_id, steps_id, cell_x_id, cell_y_id+1, id, 'east')

        else:
            if hwall_id[wall_x][wall_y]:
                if (wall_x == cell_x_id and wall_y == cell_y_id):
                    id_propagation(vwall_id, hwall_id, cells_id, steps_id, cell_x_id-1, cell_y_id, id, 'north')
                        
                else:
                    id_propagation(vwall_id, hwall_id, cells_id, steps_id, cell_x_id+1, cell_y_id, id, 'south')

def gen_laby_unp(vwall_laby, hwall_laby, cell_laby, L_laby, l_laby):
    '''Genre notre labyrinthe'''
    v_interior = get_vert_interiror(vwall_laby)
    h_interior = get_horiz_interiror(hwall_laby)

    steps = gen_steps(get_wall_coords(v_interior, h_interior))
    wall_count = get_wall_count(v_interior, h_interior)
    wall_left = (L_laby-1)*(l_laby-1)

    while wall_count > wall_left:
        wall = steps.pop(0)
        wall_x = wall[1][0]
        wall_y = wall[1][1]

        if wall[0] == 0:
            if cell_laby[wall_x][wall_y] != cell_laby[wall_x][wall_y+1]:
                if cell_laby[wall_x][wall_y] < cell_laby[wall_x][wall_y+1]:
                    id_propagation(vwall_laby, hwall_laby, cell_laby, steps, wall_x, wall_y+1, cell_laby[wall_x][wall_y], 'east')
                else:
                    id_propagation(vwall_laby, hwall_laby, cell_laby, steps, wall_x, wall_y, cell_laby[wall_x][wall_y+1], 'west')
                
                vwall_laby[wall_x][wall_y+1] = True
        else:
            if cell_laby[wall_x][wall_y] != cell_laby[wall_x+1][wall_y]:
                if cell_laby[wall_x][wall_y] < cell_laby[wall_x+1][wall_y]:
                    id_propagation(vwall_laby, hwall_laby, cell_laby, steps, wall_x+1, wall_y, cell_laby[wall_x][wall_y], 'south')
                else:
                    id_propagation(vwall_laby, hwall_laby, cell_laby, steps, wall_x, wall_y, cell_laby[wall_x+1][wall_y], 'north')
                hwall_laby[wall_x+1][wall_y] = True

        wall_count = get_wall_count(get_vert_interiror(vwall_laby), get_horiz_interiror(hwall_laby))

        ##--DEBUG--##
        #displayer(labydisplayer(vwall_laby, hwall_laby, cell_laby, L_laby, l_laby, '+', '─', '|', True))
        ##-DEBUG--##

    return cell_laby, vwall_laby, hwall_laby

def labydisplayer(vwall, hwall, cell, L, l, corner, txwall, tywall, debug):
    '''generer notre labyrinthe visible dans la console'''
    laby_L = 2*L+1
    laby_l = 2*l+1

    laby = [[" " for i in range(laby_l)] for j in range(laby_L)]
    
    for i in range(laby_L):
        for j in range(laby_l):
            
            if is_pair(i) :
                
                if is_pair(j):
                    laby[i][j] = corner
                else:
                    if not hwall[int(i/2)][int((j-1)/2)]:
                        laby[i][j] = txwall

            else:

                if is_pair(j):
                    if not vwall[int((i-1)/2)][int(j/2)]:
                        laby[i][j] = tywall
                elif debug:

                    laby[i][j] = cell[int((i-1)/2)][int((j-1)/2)]
    return laby

def displayer(matrix_disp):
    '''affiche une matrice'''
    print()
    for i in matrix_disp:
        s = ""
        for j in i:
            s = s + str(j) + " "
            
        print(s)