import logging
import triangle.array_util as util

# 0 = flat step
# 1 = down step

row_dict = dict();
row_dict[1] = [[k, ] for k in range(0, 2)]

def get_row(size):
    if not size in row_dict:
        prev_list = get_row(size-1)
        new_list1 = [ [0, ] + p for p in prev_list]
        new_list2 = [ [1, ] + p for p in prev_list]
        new_list = new_list1 + new_list2

        row_dict[size] = new_list

    return row_dict[size]

triangle_dict = dict()
triangle_dict[1] = [[[k, ],  ] for k in range(0, 2)]


# 0 = flat step
# 1 = down step
def get_binary_triangle(size):
    if not size in triangle_dict:
        prev_list = get_binary_triangle(size-1)
        row_list = get_row(size)
        triangle_list = []

        for row in row_list:
            for prev in prev_list:
                triangle_list.append(prev + [row, ] )


        triangle_dict[size] = triangle_list

    return triangle_dict[size]


def get_uncombed_triangles(size):
    binary_list = get_binary_triangle(size)
    uncombed_list = [get_omega_for_cliff(b) for b in binary_list]


    return uncombed_list

def get_combed_triangles(size):
    binary_list = get_binary_triangle(size)

    combed_list = []
    for t in binary_list:
        B,D = comb(t)
        combed_list.append(get_omega(B,D))

    return combed_list

def get_all_zero(size):
    return [[0] * k for k in range(1,size+1)]


# untangle rows i and i+1 up to column k
def untangle(B, D, i, k):
    #print('untangle', i, k, B, D)
    cur = 0
    d = 0

    logging.debug('\t\t\ti=%s k%s', i, k)
    logging.debug('\t\t\tbefore')
    logging.debug('\t\t\t\t%s', B)
    logging.debug('\t\t\t\t%s', D)
    logging.debug('\t\t\t\tomega')
    logging.debug('\t\t\t\t%s', get_omega(B,D))

    #logging.debug('new untangle!!!!!!!') #THIS IS WHAT I'M TRYING TO FIGURE OUT

    for j in range(k+1):
        # ORIGINAL
        cur = cur + B[i+1][j] - B[i][j]
        # BALLOT?
        #cur = cur + B[i + 1][j] + D[i+1][j] - B[i][j] - D[i+1][j]
        #logging.debug('cur', cur, 'd', d)
        if cur > d:
            d = cur
            #logging.debug('$$$$$$$$$$$ hit it')
            # interchange direction of steps
            B[i][j] = 1
            B[i+1][j] = 0
    # transfer d vertical steps to P_{i+1}
    D[i][k] = D[i][k] - d
    # ORIGINAL
    D[i+1][k] = d
    # BALLOT?
    #D[i+1][k] = D[i+1][k] + d
    #logging.debug('untangle returning', i, k, B, D)

    logging.debug('\t\t\tafter')
    logging.debug('\t\t\t\t%s', B)
    logging.debug('\t\t\t\t%s', D)
    logging.debug('\t\t\t\tomega')
    logging.debug('\t\t\t\t%s', get_omega(B, D))

    return B,D

#  had to fix the initialization of D[k][k]
def get_down_for_cliff(B):
    size = len(B)
    D = get_all_zero(size)
    for k in range(size):
        #logging.debug('B[k]', k, B[k])
        D[k][k] = k+1- sum([B[k][j] for j in range(k+1)])
    return D

#  had to fix the initialization of D[k][k]
def comb(binary_triangle):
    down_triangle = get_all_zero(len(binary_triangle))

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

    #print('zzzzzzzzzzzzzz')
    #util.print_array(B)
    #util.print_array(D)

    for k in reversed(range(size)):
        logging.debug('\tcomb row %s', k)
        #D[k][k] =  sum([B[k][j] for j in range(k+1)])
        D[k][k] = k+1 - sum([B[k][j] for j in range(k+1)])
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


def print_triangle(t):
    for row in t:
        print(row)
    print('---------')

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
    else:
        row[0] = abs(row[0])

    return row

def get_omega(B,D):
    omega = [ to_omega_row(b_row, d_row,) for b_row, d_row in zip(reversed(B),reversed(D))]

    return omega

def get_omega_for_cliff(B):
    return get_omega(B, get_down_for_cliff(B))

# The right choice is 1=flat and 0=down
def get_std_omega_for_cliff(B):
    newB = [ [1 -x for x in row ] for row in B]
    util.print_array(newB)
    return get_omega(newB, get_down_for_cliff(newB))


def is_magog(omega_cliff):
    triangle = omega_cliff
    for idx in range(0,len(triangle)-1):
        # biggest NW diag must increase
        if abs(triangle[idx][-1]) < abs(triangle[idx+1][-1]):
            #logging.debug('failed diagonal test:', triangle)
            return False


        row = [abs(x) for x in triangle[idx]]
        next_row = [abs(x) for x in triangle[idx+1]]
        # no shared diagonals
        # no crossing
        for j in range(1, len(row)-1):
            if row[j] < row[j-1] and row[j] == next_row[j] and row[j-1] ==  next_row[j-1]:
                #logging.debug("failing", triangle)
                return False

            if row[j] < next_row[j]:
                return False

    return True


def is_supported_gog(omega):
    for row_idx in range(len(omega)-1):
        row = omega[row_idx]
        for col_idx in range(1, len(row)):
            if row[col_idx] > 0 and not abs(omega[row_idx+1][col_idx-1]) == abs(row[col_idx]):
                return False
    return True


def is_vless_gog(omega):
    for row_idx in range(len(omega)-1):
        row = omega[row_idx]
        for col_idx in range(1, len(row)):
            if row[col_idx] < 0 and not abs(row[col_idx-1]) == abs(row[col_idx]):
                return False
    return True

# this is too naive of a test!!!!
def is_binary_vless(binary):
    logging.debug('---------', binary)
    for i in range(len(binary)-1):
        small_row  = binary[i]
        big_row = binary[i+1]
        small_zero_count = 0
        big_zero_count = 0
        crossed = False
        for j in range(len(small_row)):
            if small_row[j] == 0:
                small_zero_count = small_zero_count + 1
            if big_row[j] == 0:
                big_zero_count = big_zero_count + 1

            if crossed and big_zero_count == small_zero_count:
                if big_row[j+1] == 0:
                    logging.debug('>>>>>>>>>>>>>>>>>>>>>>>next big step is 0', j, small_row, big_row)
                    return False
                else:
                    crossed = False
            if not crossed and small_zero_count == big_zero_count+1:
                crossed = True
                logging.debug('crossed', i, j, small_row, big_row)

            if crossed and i == len(small_row)-1 and big_row[i+1] == 0:
                logging.debug('last big step is 0', small_row, big_row)
                return False

    return True

# omega triangle
def to_tangle(triangle):
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


# reflected through y=x
def to_tangle2(triangle):
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


def to_ytableau(triangle):
    tex_list = [ '$\\begin{ytableau}']
    for row in triangle:
        tex_list.append(' & '.join(str(r) for r in row) + ' \\\\')
    tex_list.append('\\end{ytableau}$')

    return ' '.join(tex_list)


def to_tikz(tri_before, tri_after):
    size = len(tri_before)
    tex_list = ['\\begin{tikzpicture}[scale=.5]']
    tex_list.append('\\begin{scope}[shift={(0,0)}]')
#    tex_list.append('\\node at (' + str(-size) + ',' + str(size/2) +') {' + to_tex_ytableau(tri_before) + '};')
    tex_list.append('\\node at (' + str(-size) + ',' + str(1/2*size) +') {\scriptsize ' + to_ytableau(tri_before) + '};')

    tex_list.append(to_tangle(tri_before))
    tex_list.append('\\end{scope}')

    tex_list.append('\\begin{scope}[shift={(' + str(2*size) + ',0)}]')
    tex_list.append('\\node at (' + str(size/2) + ',' + str(3/2*size) +') {' + to_ytableau(tri_after) + '};')
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
        tex_list.append('\\node at (' + str(-3/2*size) + ',' + str(1/2*size) +') {\scriptsize' + to_ytableau(omega) + '};')

    tex_list.append(to_tangle(omega))
    tex_list.append('\\end{scope}')

    tex_list.append('\\end{tikzpicture}')
    tex_list.append('\\bigskip')
    tex_list.append('\\bigskip')

    return '\n'.join(tex_list)


def are_equal(triangle1, triangle2):
    for row1, row2 in zip(triangle1,triangle2):
        for x,y in zip(row1,row2):
            if not x == y:
                return False
    return True


#####################################################################
#####################################################################
#####################################################################
#####################################################################
if __name__ == '__main__':

    size = 2

    t_list = get_binary_triangle(size)

    #t_list =  [ [[1],[0,0],[1,1,1]] ]

    #t_list = [ t_list[1]]

    for t in t_list:
        util.print_array(t)
        omega = get_omega_for_cliff(t)
        print('omega', omega)




    omega_map = dict()
    after_set = set()
    duplicate_count = 0
    disjoint_count = 0

    magog_map  = dict()

    gog_map = dict()

    gog_bin_list =  []
    magog_bin_list = []



    binary_vless_list = []


    for before in t_list:
        after, down = comb(before)
        print("=================")
        print('before')
        print_triangle(before)
        print_triangle(get_down_for_cliff(before))
        print('omega')
        print_triangle(get_omega_for_cliff(before))
        print('after')
        print_triangle(after)
        print('down')
        print_triangle(down)
        print('omega')
        print_triangle(get_omega(after,down))

        omega_cliff = get_omega_for_cliff(before)

        omega = get_omega(after,down)

        bstr = str(get_omega_for_cliff(before))
        astr = str(omega)

        #print_array(omega)

        if astr in omega_map:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>already created', astr)
            print('\t', bstr, 'and', omega_map[astr])
            duplicate_count = duplicate_count + 1
        else:
            omega_map[astr] = bstr

        if astr == bstr:
            disjoint_count = disjoint_count + 1

        if is_magog(omega_cliff): # and not astr == bstr:
            magog_map[astr] = omega
            magog_bin_list.append(before)

        # if is_supported_gog(omega):
        #      gog_map[astr] = omega
        #      gog_bin_list.append(before)

        if is_vless_gog(omega):
            gog_map[astr] = omega
            gog_bin_list.append(before)

        after_set.add(str(after))

        if is_binary_vless(before):
            binary_vless_list.append(before)

    #################

    #print_array(get_omega([[0],[0,0],[0,0,0]], [[1],[0,2],[0,0,3]] ))

    # print("duplicates:", duplicate_count)
    # print("disjoint:", disjoint_count)
    # print("after:", len(after_set))
    # print("magog:", len(magog_map))
    # print("gog:", len(gog_map))
    #
    # magog_only_list = []
    #
    # for m in magog_map:
    #     if not m in gog_map:
    #         magog_only_list.append(magog_map[m])
    #
    # gog_only_list = []
    #
    # for g in gog_map:
    #     if not g in magog_map:
    #         gog_only_list.append(gog_map[g])
    #
    # print("magog only:", len(magog_only_list))
    # print("gog only:", len(gog_only_list))


    #####################


    # test_comb([[3, -3, 2, 1], [3, 2, 1], [1, 0], [1]],
    #           [[-4, -4, 2, 1], [-3, 1, 0], [1, 0], [0]])


    # my mapping is the reverse of theirs. weird
    #bt = [[0],[1,1],[0,1,1],[1,0,1,1]]
    #bt = [[1],[0,0],[1,0,0],[0,1,0,0]]
    #bt = [[0],[0,0]]

    #print(get_omega_for_cliff(bt))
    #bout, dout = comb(bt)
    #print(get_omega(bout, dout))


    #for m in gog_only_list:
    #    print(to_tikz_after(m))
    #    print('')


    #print('=== binary gog list')


    gog_one_count = [0] *  int(size * (size+1))
    magog_one_count = [0] * int(size * (size+1))

    print('>>>>>>>>>>>> GOG')

    for g in gog_bin_list:
    #    util.print_array(g)

        g_sum = sum( [ sum(row) for row in g])
        print('gog sum=', g_sum, g)
        gog_one_count[g_sum] = gog_one_count[g_sum] + 1

    #print('>>>>>>>>>>>> GOG ONLY')
    #    if not g in magog_bin_list:
    #        util.print_array(g)

    print('>>>>>>>>>>>> MAGOG')

    for m in magog_bin_list:
        m_sum = sum([sum(row) for row in m])
        print('magog sum=', m_sum, m)
        magog_one_count[m_sum] = magog_one_count[m_sum] + 1



    print(gog_one_count, sum(gog_one_count))
    print(magog_one_count, sum(magog_one_count))

    print('###### NOT GOG')
    for t in t_list:
        if t not in gog_bin_list:
            util.print_array(t)

    #
    # #print('=== binary magog only')
    # print('>>>>>>>>>>>> MAGOG ONLY')
    #
    # for g in magog_bin_list:
    #    if not g in gog_bin_list:
    #        util.print_array(g)

    ####################

    # print('vless=', len(binary_vless_list))
    #
    # for b in binary_vless_list:
    #     after, down = comb(b)
    #     omega = get_omega(after,down)
    #     if not is_vless_gog(omega):
    #         print('----------')
    #         print_array(b)
    #         print_array(omega)
    #
    #
    # print(is_binary_vless([[0],[1,1],[1,0,0]]))
    #
    #
    #
    # print('********* moment of truth')
    #
    # #t = [[4,3,2,1], [3,2,2], [2,2], [1]]
    # start_B = [[0],[0,0],[0,1,0],[0,1,1,1]]
    #
    # out_B, out_D  =  comb(start_B)
    #
    #
    #
    # print_array(get_omega_for_cliff(start_B))
    # print_array(get_omega(out_B, out_D))


    #print('?????????')
    #bint = [[0], [0, 1], [1,0, 1]]
    #myb, myd = comb(bint)

    #print_triangle(get_omega(myb,myd))



