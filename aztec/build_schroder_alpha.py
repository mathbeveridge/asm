
# this is Ian's first idea about Schroder columns


column_dict = dict()
column_dict[0] = [[]]
column_dict[1] = [[k, ] for k in range(0, 2)]


triangle_dict = dict()
triangle_dict[1] = [[[k, ],] for k in range(0, 2)]


# column are weakly increasing when you ignore zeros
def column_list(size):

    if not size in column_dict:

        col_list = []

        # deal with 0 and 1
        prev_list = column_list(size - 1)

        for col in prev_list:
            col_list.append([0,] + col)

        for col in prev_list:
            col_list.append([1, ] + col)

        # now deal with larger
        for k in range(2, size+1):
            colx = column_list(k-1)
            coly = column_list(size - k)

            for x in colx:
                for y in coly:
                    col_list.append([k,] + x + y)

        column_dict[size] =  col_list

    return column_dict[size]


def is_compatible(big_col, small_col):

    print(small_col)

    small_size = len(small_col)

    # every diagonal must decrease until 0
    for idx in range(small_size):
        if big_col[idx] > 0:
            if small_col[idx] >= big_col[idx]:
                print('fail small entry too big for', big_col[idx])
                return False
        elif small_col[idx] >= 1:
            print('fail small entry too big')
            return False

    # when big column completes, the corresponding small entry must be 0
    length = 0
    for idx in range(small_size):
        if length == 0:
            if big_col[idx] > 1:
                length = big_col[idx] -1
            else:
                if small_col[idx] > 0:
                    print('failing here')
                    return False
        else:
            length+=-1
            if length == 0:
                if small_col[idx] > 0:
                    print('failing there')
                    return False

    # rows must weakly decrease to 1/0
    for idx in range(small_size):
        if small_col[idx] > 1 and big_col[idx+1] < small_col[idx]:
            return False


    return True



def get_triangles(size):
    if not size in triangle_dict:
        tri_list = []
        small_list = get_triangles(size-1)
        col_list = column_list(size)

        for c in col_list:
            for tri in small_list:
                if is_compatible(c, tri[0]):
                    tri_list.append( [c,] + tri)

        triangle_dict[size] = tri_list

    return triangle_dict[size]


if __name__ == '__main__':

    #cols = column_list(5)

    #for c in cols:
    #    print(c)

    #print(len(cols))

    #bc = [3,2,1,2,1,1]
    #sc = [2,1,0,1,0]
    #print(bc,sc,is_compatible(bc,sc))

    tri_list = get_triangles(3)

    for t in tri_list:
        print(t)

    print(len(tri_list))