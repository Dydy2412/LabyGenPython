##--Dydy2412--##
def labydisplayer(vwall, hwall, cell, L, l, corner, txwall, tywall, debug):
    '''generer notre labyrinthe visible dans la console'''
    laby_L = 2*L+1
    laby_l = 2*l+1

    laby = [[" " for i in range(laby_l)] for j in range(laby_L)]
    
    for i in range(laby_L):
        for j in range(laby_l):
            
            if i%2 == 0:
                
                if j%2 == 0:
                    laby[i][j] = corner
                else:
                    if not hwall[int(i/2)][int((j-1)/2)]:
                        laby[i][j] = txwall

            else:

                if j%2 == 0:
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