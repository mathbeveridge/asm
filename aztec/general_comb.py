# trying to write a comber that will handle vertical steps

import logging
import triangle.array_util as util
import triangle.build_binary_triangle as bbt

# 0 = flat step
# 1 = down step




# untangle rows i and i+1 up to column k
def untangle(B, D, i, k):
    #print('untangle', i, k, B, D)

    # the current separation of the paths
    cur = 1 # the low path is below by 1 unit
    # the current shift amount
    d = 1

    logging.debug('\t\t\tuntangle')
    logging.debug('\t\t\ti=%s k%s', i, k)
    logging.debug('\t\t\tbefore')
    logging.debug('\t\t\t\tB=%s', B)
    logging.debug('\t\t\t\tD=%s', D)
    logging.debug('\t\t\t\tomega')
    logging.debug('\t\t\t\t%s', get_omega(B,D))

    #logging.debug('new untangle!!!!!!!') #THIS IS WHAT I'M TRYING TO FIGURE OUT

    for j in range(k+1):
        cur = cur - B[i + 1][j] - D[i+1][j] + B[i][j]
        logging.debug('j %s cur %s d %s', j, cur, d)
        if cur > 0:
            cur = cur + D[i][j]
        else:
            logging.debug('$$$$$$$$$$$ hit it')
            if B[i][j] == 0:
                # the smaller path just took a horizontal step
                if D[i][j] == 0:
                    # no drop in the smaller path
                    big_drop_idx = -1
                    for jj in reversed(range(j)):
                        if D[i+1][jj] > 1:
                            big_drop_idx == jj
                            break
                    if big_drop_idx >= 0:
                        print('USING BIG DROP', jj)
                        # previous vertical drop of the bigger path  can absorb
                        D[i+1][big_drop_idx] = D[i+1][big_drop_idx] - 1
                        D[i+1][j] = D[i+1][j] + 1
                        B[i][j]=1
                    else:
                        # interchange direction of steps
                        B[i][j] = 1
                        B[i+1][j] = 0
                        D[i+1][k] = D[i+1][k] + 1 # put the extra drop in the last possible place
                        # find the down step to absorb. The first one? The matching one?
                    idx = j
                    while D[i][idx] == 0 :
                        idx += 1
                    D[i][idx] = D[i][idx] - 1
                    cur = 2 + D[i][j]
                else:
                    # use the drop in the smaller path
                    B[i][j] = 1
                    D[i][j] = D[i][j]-1
                    # look for drop in larger path
                    big_drop_idx = -1
                    for jj in reversed(range(j)):
                        if D[i+1][jj] >= 1:
                            big_drop_idx = jj
                            break
                    if big_drop_idx >= 0:
                        print('UPDATING BIG DROP')
                        D[i+1][big_drop_idx] = D[i+1][big_drop_idx] - 1
                        D[i + 1][j] = D[i + 1][j] + 1
                    else:
                        B[i + 1][j] = 0
                        D[i + 1][j] = D[i + 1][j] + 1
            else:
                # the smaller path just took a down step so the upper path has a drop
                # change smaller step to flat (drop is still fine)
                B[i][j] = 0
                D[i][j-1] = D[i][j-1] + 1
                # move upper drop to position k
                D[i+1][j] = D[i+1][j] - 1 # NEED TO FIX LATER?
                D[i+1][k] = D[i+1][k] + 1
                cur = 2 + D[i][j] # probably not right?



    logging.debug('\t\t\tafter')
    logging.debug('\t\t\t\t%s', B)
    logging.debug('\t\t\t\t%s', D)
    logging.debug('\t\t\t\tomega')
    logging.debug('\t\t\t\t%s', get_omega(B, D))

    return B,D

#  had to fix the initialization of D[k][k]
def get_down_for_cliff(B):
    size = len(B)
    D = util.get_all_zero_triangle(size)
    for k in range(size):
        #logging.debug('B[k]', k, B[k])
        D[k][k] = k+1- sum([B[k][j] for j in range(k+1)])
    return D

#  had to fix the initialization of D[k][k]
def comb(binary_triangle):
    size = len(binary_triangle)
    down_triangle = util.get_all_zero_triangle(len(binary_triangle))

    for k in reversed(range(size)):
        down_triangle[k][k] = k+1 - sum([binary_triangle[k][j] for j in range(k+1)])

    return comb_BD(binary_triangle, down_triangle)
    #size = len(binary_triangle)
    #B = [[x for x in row] for row in binary_triangle]
    #D = get_all_zero_triangle(size)

    #logging.debug('combing', B, D)

    # for k in reversed(range(size)):
    #     #D[k][k] =  sum([B[k][j] for j in range(k+1)])
    #     D[k][k] = k+1 - sum([B[k][j] for j in range(k+1)])
    #     for i in range(k,size-1):
    #         B,D = untangle(B,D,i,k)
    #
    # return B,D

def comb_BD(binary_triangle, down_triangle):
    size = len(binary_triangle)
    B = [[x for x in row] for row in binary_triangle]
    D = [[x for x in row] for row in down_triangle]

    logging.debug('comb_DB start')
    logging.debug(str(B))
    logging.debug(str(D))
    logging.debug('omega')
    logging.debug(str(get_omega(B,D)))

    util.print_array(B)
    util.print_array(D)

    for k in reversed(range(size)):
        logging.debug('\tcomb row %s', k)
        for i in range(k,size-1):
            B,D = untangle(B,D,i,k)
            logging.debug('\tuntangle %s %s', i, k)
            logging.debug('\t\t  %s', B)
            logging.debug('\t\t  %s', D)

    logging.debug('comb_DB returning')
    logging.debug(str(B))
    logging.debug(str(D))
    logging.debug('omega')
    logging.debug(str(get_omega(B, D)))
    logging.debug('++++++++++++++++++++++++')

    return B,D




# remember: b=1 is a down step, b=0 is a flat step
def to_omega_row(b_row, d_row):
    row = []
    height = 0

    for b,d in zip(reversed(b_row), reversed(d_row)):
        height = height + d
        val = (-1)**(b+1)  *  height
        row.insert(0, val)
        if b == 1:
            height = height + 1

    size = len(b_row)
    if abs(row[0]) < size:
        row[0] = abs(row[0])

    return row

def get_omega(B,D):
    omega = [ to_omega_row(b_row, d_row,) for b_row, d_row in zip(reversed(B),reversed(D))]

    return omega

def get_omega_for_cliff(B):
    return get_omega(B, get_down_for_cliff(B))





def to_tangle(omega):
    triangle = omega
    size = len(triangle)
    path_list = []

    for row_idx in range(size):
        row = triangle[row_idx]
        row_size = len(row)
        my_path =  ['\draw[thick] (-1, ' + str(row_size) + ') -- (0, ' \
                  + str(abs(row[0])) + ')']
        for col_idx in range(1, row_size):
            height = row[col_idx]
            prev_idx = col_idx - 1
            if height < 0:
                my_path.append(' -- (' + str(prev_idx) + ',' + str(abs(height)) + ')' )
            elif abs(row[col_idx-1]) > abs(height):
                my_path.append(' -- (' + str(prev_idx) + ',' + str(abs(height)+1) + ')' )


            my_path.append(' -- (' + str(col_idx) + ',' + str(abs(height)) + ')')

        if not row[row_size-1] == 0:
            my_path.append(' -- (' + str(row_size-1) + ',0)')

        my_path.append(';')

        path_list.append( ' '.join(my_path))

    return('\n'.join(path_list))



def to_tangle2(omega):
    triangle = omega
    size = len(triangle)
    path_list = []

    for row_idx in range(size):
        row = triangle[row_idx]
        row_size = len(row)
        my_path =  ['\draw[thick] (' + str(row_size) + ',-1) -- (' \
                  + str(abs(row[0])) + ',0)']
        for col_idx in range(1, row_size):
            height = row[col_idx]
            prev_idx = col_idx - 1
            if height < 0:
                my_path.append(' -- (' + str(abs(height)) + ','+ str(prev_idx)  + ')' )
            elif abs(row[col_idx-1]) > abs(height):
                my_path.append(' -- (' + str(abs(height)+1) + ',' + str(prev_idx) + ')' )


            my_path.append(' -- (' + str(abs(height)) + ','+ str(col_idx)  + ')')

        if not row[row_size-1] == 0:
            my_path.append(' -- (0,' + str(row_size-1) + ')')

        my_path.append(';')

        path_list.append( ' '.join(my_path))

    return('\n'.join(path_list))


def to_tikz(tri_before, tri_after):
    size = len(tri_before)
    tex_list = ['\\begin{tikzpicture}[scale=.5]']
    tex_list.append('\\begin{scope}[shift={(0,0)}]')
#    tex_list.append('\\node at (' + str(-size) + ',' + str(size/2) +') {' + to_tex_ytableau(tri_before) + '};')
    tex_list.append('\\node at (' + str(-size) + ',' + str(1/2*size) +') {\scriptsize ' + util.to_ytableau(tri_before) + '};')

    tex_list.append(to_tangle(tri_before))
    tex_list.append('\\end{scope}')

    tex_list.append('\\begin{scope}[shift={(' + str(2*size) + ',0)}]')
    tex_list.append('\\node at (' + str(size/2) + ',' + str(3/2*size) +') {' + util.to_ytableau(tri_after) + '};')
    tex_list.append(to_tangle(tri_after))
    tex_list.append('\\end{scope}')
    tex_list.append('\\end{tikzpicture}')
    tex_list.append('\\bigskip')
    tex_list.append('\\bigskip')

    return '\n'.join(tex_list)


def to_tikz_after(omega, show_omega):
    size = len(omega)
    tex_list = ['\\begin{tikzpicture}[scale=.5]']
    tex_list.append('\\begin{scope}[shift={(0,0)}]')
    if show_omega:
        tex_list.append('\\node at (' + str(-3/2*size) + ',' + str(1/2*size) +') {\scriptsize' + util.to_ytableau(omega) + '};')

    tex_list.append(to_tangle(omega))
    tex_list.append('\\end{scope}')

    tex_list.append('\\end{tikzpicture}')
    tex_list.append('\\bigskip')
    tex_list.append('\\bigskip')

    return '\n'.join(tex_list)





def test():
    size = 3

    t_list = bbt.get_binary_triangle(size)

    t_list = [[row for row in reversed(t)] for t in t_list]

    # t_list =  [ [[1],[0,0],[1,1,1]] ]

    # t_list = [ t_list[1]]


    omega_map = dict()
    after_set = set()
    duplicate_count = 0
    disjoint_count = 0

    magog_map = dict()

    gog_map = dict()

    gog_bin_list = []
    magog_bin_list = []

    binary_vless_list = []

    for before in t_list:
        after, down = comb(before)
        print("=================")
        print('before')
        util.print_array(before)
        util.print_array(get_down_for_cliff(before))
        print('omega')
        util.print_array(get_omega_for_cliff(before))
        print('after')
        util.print_array(after)
        print('down')
        util.print_array(down)
        print('omega')
        util.print_array(get_omega(after, down))

        omega_cliff = get_omega_for_cliff(before)

        omega = get_omega(after, down)

        bstr = str(get_omega_for_cliff(before))
        astr = str(omega)

        # print_array(omega)

        if astr in omega_map:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>already created', astr)
            print('\t', bstr, 'and', omega_map[astr])
            duplicate_count = duplicate_count + 1
        else:
            omega_map[astr] = bstr

        if astr == bstr:
            disjoint_count = disjoint_count + 1

        after_set.add(str(after))


#####################################################################
#####################################################################
#####################################################################
#####################################################################
if __name__ == '__main__':




    #################

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    print('latest stuff')

    # myB = [[0,1,0],[1,0],[0]]
    # myD = [[1,0,1],[0,1],[1]]
    #
    # myB = [x for x in reversed(myB)]
    # myD = [x for x in reversed(myD)]


    myB = [[1], [0, 1], [0, 0, 1]]
    myD = [[0], [1, 0], [0, 2, 0]]


    outB, outD = comb_BD(myB, myD)

    util.print_array(get_omega(myB, myD))

    util.print_array(get_omega(outB, outD))