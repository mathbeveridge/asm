import triangle.array_util as util
import logging


row_dict = dict()
row_dict[1] =[[k, ] for k in range(0, 2)]
row_dict[0] = [(0,), ]


def get_row(size):
    if size not in row_dict:
        row_list = []
        prev_list = get_row(size-1)
        for idx in range(size+1):
            for prev in prev_list:
                if idx >= prev[-1]:
                    row_list.append(prev + [idx,])

        row_dict[size] = row_list

    return row_dict[size]

kagog_row_dict = dict()
kagog_row_dict[1] =[[k, ] for k in range(0, 2)]
kagog_row_dict[0] = [(0,), ]


def get_kagog_row(size):
    if size not in kagog_row_dict:
        row_list = []
        prev_list = get_kagog_row(size-1)

        for prev in prev_list:
            if prev[-1] == 0:
                start = 0
            else:
                start = prev[-1] + 1

            for idx in range(start, size+1):
                row_list.append(prev + [idx,])

        kagog_row_dict[size] = row_list

    return kagog_row_dict[size]


bigog_dict = dict()
bigog_dict[1] = [[[k, ],] for k in range(0,2)]

magog_dict = dict()
magog_dict[1] = [[[k, ],] for k in range(0,2)]

kagog_dict = dict()
kagog_dict[1] = [[[k, ],] for k in range(0,2)]

gog_dict = dict()
gog_dict[1] = [[[k, ],] for k in range(0,2)]

def get_bigog(size):
    if not size in bigog_dict:
        new_list = []
        prev_list = get_bigog(size-1)
        row_list = get_row(size)

        for row in row_list:
            for prev in  prev_list:
                is_compatible = True
                for idx in range(len(prev)):
                    if prev[0][idx] < row[idx]:
                        is_compatible = False
                        break

                if is_compatible:
                    new_list.append([row] + prev)

        bigog_dict[size] = new_list

    return bigog_dict[size]

def get_magog(size):
    if not size in magog_dict:
        new_list = []
        prev_list = get_magog(size-1)
        row_list = get_row(size)

        for row in row_list:
            for prev in  prev_list:
                is_compatible = True
                for idx in range(len(prev)):
                    if prev[0][idx] < row[idx]:
                        is_compatible = False
                        break
                    elif prev[0][idx] > row[idx+1]:
                        is_compatible = False
                        break

                if is_compatible:
                    new_list.append([row] + prev)

        magog_dict[size] = new_list

    return magog_dict[size]


def get_kagog(size):
    if not size in kagog_dict:
        new_list = []
        prev_list = get_kagog(size-1)
        row_list = get_kagog_row(size)

        for row in row_list:
            for prev in  prev_list:
                is_compatible = True
                for idx in range(len(prev)):
                    if prev[0][idx] < row[idx]:
                        is_compatible = False
                        break

                if is_compatible:
                    new_list.append([row] + prev)

        kagog_dict[size] = new_list

    return kagog_dict[size]



def get_gog(size):
    if not size in gog_dict:
        new_list = []
        prev_list = get_gog(size-1)
        row_list = get_row(size)

        for row in row_list:
            for prev in  prev_list:
                is_compatible = True
                for idx in range(len(prev)):
                    if prev[0][idx] < row[idx]:
                        is_compatible = False
                        break
                    elif prev[0][idx] < row[idx+1] -1:
                        is_compatible = False
                        break

                if is_compatible:
                    new_list.append([row] + prev)

        gog_dict[size] = new_list

    return gog_dict[size]




def count_subtriangles(size):
    print('*************')
    gog_list = get_gog(size)
    magog_list = get_magog(size)
    kagog_list = get_kagog(size)

    count = 0


    print('GOG ONLY')
    gog_not_magog_list = []
    gog_not_kagog_list = []
    all_list = []
    for x in gog_list:
        if x not in magog_list:
            gog_not_magog_list.append(x)
        elif x in kagog_list:
            all_list.append(x)
        if x not in kagog_list:
            gog_not_kagog_list.append(x)

    for k in gog_not_kagog_list:
        util.print_array(k)

    print('gog not magog', len(gog_not_magog_list))
    print('gog not kagog', len(gog_not_kagog_list))

    print('MAGOG ONLY')
    magog_not_gog_list = []
    magog_not_kagog_list = []
    for x in magog_list:
        if x not in gog_list:
            magog_not_gog_list.append(x)
        if x not in kagog_list:
            magog_not_kagog_list.append(x)

    print('magog not gog', len(magog_not_gog_list))
    print('magog not kagog', len(magog_not_kagog_list))

    #print(len(magog_only))
    #print(count)




    print('KAGOG ONLY')
    kagog_not_gog_list = []
    kagog_not_magog_list = []
    for x in kagog_list:
        if x not in gog_list:
            kagog_not_gog_list.append(x)
        if x not in magog_list:
            kagog_not_magog_list.append(x)

    for k in kagog_only:
        util.print_array(k)
    print('kagog not gog', len(kagog_not_gog_list))
    print('kagog not magog', len(kagog_not_magog_list))


    count = len(gog_list)
    print('gog and magog', count - len(gog_not_magog_list))
    print('gog and kagog', count - len(gog_not_kagog_list))
    print('magog and kagog', count - len(magog_not_kagog_list))
    print('all three', len(all_list))


    #for k in gog_not_kagog_list:
    #    util.print_array(k)


def uplift(triangle):
    size = len(triangle)
    uplift = [[ x + idx for x in row ] for idx, row in enumerate(triangle)]

    return uplift


def jeu_update(triangle, row_idx, col_idx):
    #print('\t\t\t',row_idx, col_idx)

    size = len(triangle)

    debug('jeu update row %s col %s triangle %s', row_idx, col_idx, triangle)

    if row_idx > 0 and col_idx < size -1:

        # in general, looking at entries of the form:
        #   bz
        #  ay
        #  x
        # where we replace c and d with size+1 when they do not exist

        a = triangle[row_idx][col_idx]
        b = triangle[row_idx - 1][col_idx + 1]

        if row_idx == size - 1 - col_idx:
            # on the lowest diagonal
            x = size+1
            y = size+1
            z = size+1
        else:
            x = triangle[row_idx+1][col_idx]
            y = triangle[row_idx][col_idx + 1]
            z = triangle[row_idx - 1][col_idx + 2]

        debug('-%s%s', b, z)
        debug('%s%s', a, y)
        debug('%s', x)


        if a > b:
            # must update this diagonal pair and create a diagonal gap


            if a < y:
                a = a + 1
                # swap a/b to b/a
                triangle[row_idx - 1][col_idx + 1] = a
                triangle[row_idx][col_idx] = b
            else:
                if a == y:
                    # don't increase a  (yet)
                    # swap a/b/y to b/a/y
                    triangle[row_idx - 1][col_idx + 1] = a
                    triangle[row_idx][col_idx] = b
                    a = a + 1
                else:
                    # swap a/b/y to b/y/a
                    a = a + 1
                    triangle[row_idx][col_idx] = b
                    triangle[row_idx - 1][col_idx + 1] = y
                    triangle[row_idx][col_idx + 1] = a

                diff = a - y
                # must percolate the changes down the diagonal
                for k in range(0,col_idx+1):

                    row_idx2 = row_idx + 1 + k
                    col_idx2 = col_idx - k
                    if triangle[row_idx2][col_idx2] > 0:
                        #debug('row %s col %s', str(row_idx+k), str(col_idx-k))
                        temp = min(diff, triangle[row_idx2][col_idx2])
                        triangle[row_idx2][col_idx2] +=  - temp
                    else:
                        # zeros all the way down
                        break
                # must percolate the changes up the diagonal
                for k in range(1,row_idx+1):
                    row_idx2 = row_idx - k
                    col_idx2 = col_idx + 1 + k
                    new_val = min(size, triangle[row_idx2][col_idx2] + diff)
                    triangle[row_idx2][col_idx2] =  new_val


            debug('updated', row_idx, col_idx)
            #util.print_array(triangle)

    return triangle

# recursive implementation of the game
# columnwise is not correct.
def taquin_v1(triangle, row_idx, col_idx):
    size = len(triangle)
    #print('\t\ttaquin', row_idx, col_idx)

    triangle = jeu_update(triangle, row_idx, col_idx)

    if row_idx > 0:
        triangle = taquin(triangle, row_idx - 1, col_idx)
    elif col_idx < size - 1:
        triangle = taquin(triangle, size - 2 - col_idx, col_idx +1)


    return triangle

# recursive implementation of the game
# diagonalwise should be better
# do a full diagonal and then the next.
def taquin(triangle, row_idx, col_idx):
    size = len(triangle)
    #print('\t\ttaquin', row_idx, col_idx, triangle)

    # process up the current diagonal
    for k in range(0, row_idx+1):
        triangle = jeu_update(triangle, row_idx - k, col_idx + k)


    for j in range(row_idx + col_idx + 1, size):
        for k in range(0, j):
            #print(j,k, triangle)
            triangle = jeu_update(triangle, j-k,k)


    if col_idx > 0:
        triangle = taquin(triangle, row_idx  + 1, col_idx -1)
    elif row_idx < size - 1:
        triangle = taquin(triangle, 0, row_idx +1)


    return triangle

# start with a gog
# try to get closer to a magog
def jeu_de_taquin(gog_triangle):

    # make a copy to update
    triangle = [ [x for x in row] for row in gog_triangle]

    size = len(triangle)

    #print('start')
    #util.print_array(triangle)

    for col_idx in range(0, size):
        #print('col',  size - 1 - col_idx)
        for row_idx in range(col_idx+1):
            #print('\trow', row_idx)

            triangle = taquin(triangle, row_idx, size - 1 - col_idx)

    return triangle



# Trying Krattenheller

# content is j-i
def krat_swap(triangle, row_idx, col_idx):
    size = len(triangle)
    upper_bound = max ( [max(row) for row in triangle])+1

    #print('krat swap', row_idx, col_idx)

    ret_row_idx = row_idx
    ret_col_idx = col_idx

    if True: #(row_idx + col_idx) <  size - 1:
        #print('making a change', row_idx, col_idx)
        s = triangle[row_idx][col_idx]

        if col_idx >= len(triangle[row_idx]) -1:
            x = upper_bound
        else:
            x = triangle[row_idx][col_idx+1]


        if row_idx == len(triangle) - 1 or len(triangle[row_idx+1]) < col_idx +1:
            y = upper_bound
        else:
            y = triangle[row_idx+1][col_idx]

        if s > x or s >= y:
            if x+1 < y:
                triangle[row_idx][col_idx] = x+1
                triangle[row_idx][col_idx + 1] = s
                ret_row_idx = row_idx
                ret_col_idx = col_idx +1
            else:
                triangle[row_idx][col_idx] = y-1
                triangle[row_idx + 1][col_idx] = s
                ret_row_idx = row_idx + 1
                ret_col_idx = col_idx

    return ret_row_idx, ret_col_idx

def krat_jt(triangle, row_idx, col_idx):
    old_row_idx = -1
    old_col_idx = -1

    while not (old_row_idx == row_idx and old_col_idx == col_idx):
        old_row_idx = row_idx
        old_col_idx = col_idx
        row_idx, col_idx = krat_swap(triangle, row_idx, col_idx)

    # no return value (pass triangle by value)
    return triangle



def krat(triangle_in):
    size = len(triangle_in)

    triangle = [ [x for x in row] for row in triangle_in]


    for col_idx in reversed(range(size)):
        for row_idx in reversed(range(size - col_idx)):
            #print(col_idx, row_idx)
            krat_jt(triangle, row_idx, col_idx)

    return triangle

debug_on = False

def debug(msg, *args):
    if debug_on:
        print(msg % args)



def jeu_test():

    #debug_on = True

    size = 3
    gog_list = get_gog(size)
    magog_list = get_magog(size)

    #gog = [[0,0,0],[0,1],[0]]

    error_list = []
    magog_map = dict()

    for gog in gog_list:
        jeu = jeu_de_taquin(gog)
        #print(gog)
        #print(jeu)
        if jeu not in magog_list:
            error_list.append([gog, jeu])
        #    print('\t NOT MAGOG!!!')
        else:
            if str(jeu) in magog_map:
                magog_map[str(jeu)].append(gog)
                print('multimap:', magog_map[str(jeu)])
            else:
                magog_map[str(jeu)] = [jeu, gog]


        #print('----------')

    print('ERRORS!!!!!!')
    for error in error_list:
        util.print_array(error[0])
        util.print_array(error[1])
        print('----------')

    print('num error', len(error_list))

    print(len(magog_map))



    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    #logging.basicConfig(level=logging.DEBUG)





    #t = [[0,0,0,4],[0,1,1],[0,1],[1]]
    #t = [[0, 0, 0, 1], [0, 1, 1], [0, 2], [1]]
    #t = [[0, 0, 0, 4], [0, 1, 1], [0, 1], [1]]
    # t = [[0, 0, 0, 1],[0, 1, 1],[1, 1],[1]]
    # t = [[0, 0, 1, 3], [0, 0, 1], [1, 0], [0]]
    t = [[0, 0, 2], [1, 1], [1]]

    util.print_array(t)

    s = jeu_update(t,1,0)

    #s = jeu_de_taquin(t)

    util.print_array(s)

    if s in magog_list:
        print('success')
    else:
        print('failed!!!!')


def test_krat(size):
    print('*************')
    gog_list = get_gog(size)
    magog_list = get_magog(size)
    kagog_list = get_kagog(size)

    count = 0


    print('GOG ONLY')
    gog_not_magog_list = []
    gog_not_kagog_list = []
    all_list = []
    for x in gog_list:
        if x not in magog_list:
            gog_not_magog_list.append(x)
        elif x in kagog_list:
            all_list.append(x)
        if x not in kagog_list:
            gog_not_kagog_list.append(x)

    tiered_gog_list = []

    for k in gog_list:
        tiered_gog_list.append([ [x + idx for x in row] for idx, row in zip(range(1,size+1), k)])
        #util.print_array(k)

    #for t in tiered_gog_list:
    #    print(t)



    print('MAGOG ONLY')
    magog_not_gog_list = []
    magog_not_kagog_list = []
    for x in magog_list:
        if x not in gog_list:
            magog_not_gog_list.append(x)
        if x not in kagog_list:
            magog_not_kagog_list.append(x)

    print('magog not gog', len(magog_not_gog_list))
    print('magog not kagog', len(magog_not_kagog_list))

    #print(len(magog_only))
    #print(count)


    tiered_magog_list = []

    for k in magog_list:
        tiered_magog_list.append([ [x + idx for x in row] for idx, row in zip(range(1,size+1), k)])
        #util.print_array(k)

    #for t in tiered_magog_list:
    #    print(t)




    print('KAGOG ONLY')
    kagog_not_gog_list = []
    kagog_not_magog_list = []
    for x in kagog_list:
        if x not in gog_list:
            kagog_not_gog_list.append(x)
        if x not in magog_list:
            kagog_not_magog_list.append(x)

    tiered_kagog_list = []

    for k in kagog_list:
        tiered_kagog_list.append([ [x + idx for x in row] for idx, row in zip(range(1,size+1), k)])
        #util.print_array(k)

    #for t in tiered_kagog_list:
    #    print(t)

    #    util.print_array(k)
    print('kagog not gog', len(kagog_not_gog_list))
    print('kagog not magog', len(kagog_not_magog_list))


    count = len(gog_list)
    print('gog and magog', count - len(gog_not_magog_list))
    print('gog and kagog', count - len(gog_not_kagog_list))
    print('magog and kagog', count - len(magog_not_kagog_list))
    print('all three', len(all_list))


    not_gog_list= []
    not_magog_list = []
    not_kagog_list = []

    for k in tiered_kagog_list:
        s = [[ x for x in reversed(row)] for row in k]
        #s = [[ size+2 - x for x in row] for row in k]
        s = k
        t = krat(s)

        print(s)
        #print(t)
        if t not in tiered_gog_list:
            #print('t is not a gog')
            not_gog_list.append(t)
        if t not in tiered_kagog_list:
            #print('t is not a kagog')
            not_kagog_list.append(t)
        if t not in tiered_magog_list:
            #print('t is not a magog')
            not_magog_list.append(t)

        #print('---------')

    print('not gog', len(not_gog_list))
    print('not kagog', len(not_kagog_list))
    print('not magog', len(not_magog_list))





    #for k in gog_not_kagog_list:
    #    util.print_array(k)


if __name__ == '__main__':


    #examp = [[4,1,2,2,3,4], [4,6,3,4,4], [8,5,5,5,6], [6,6,7,7]]
    #util.print_array(examp)

    #util.print_array(krat_jt(examp, 1, 1))

    s = [[1,1,1],[3,3],[3]]


    s = [[0, 0, 2],[1, 1],[1]]
    s = [[3,1, 1], [3, 3], [4]]

    #t = krat(s)

    #print(s)
    #print(t)

    #test_krat(2)

    size = 3

    k_list = [ uplift(k) for k in get_kagog(size)]
    g_list = [ uplift(g) for g in get_gog(size)]

    print('=======kagog only')
    for k in k_list:
        if k not in g_list:
            util.print_array(k)

    print('=======gog only')
    for g in g_list:
        if g not in k_list:
            util.print_array(g)

