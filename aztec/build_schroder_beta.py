import triangle.array_util as util
import aztec.binary_comb as binary_comb
import aztec.binary_layers as binary_layers

### NOTE: you can get http://oeis.org/search?q=2%2C6%2C22%2C92%2C426%2C2150&sort=&language=english&go=Search
### if you "reset" the columns at the zeros


### This family generated on 11 Feb. We are decomposing binary triangles into a nice Schroder family.
### This is actually Gamma Triangles.

### If we push the other way, we get a kagog like family: maybe they are the ones that don't need the zeros
### as filler.

# column are weakly increasing when you ignore zeros


col_map = dict();
col_map[1] = [[k, ] for k in range(0, 2)]

beta_map = dict();
beta_map[1] = [[[k, ],] for k in range(0, 2)]

def column_list(size):
    if not size in col_map:
        col_list = []
        prev_list = column_list(size - 1)
        for x in range(0,size + 1):
            for prev_col in prev_list:
                if x == 0 or x >= max(prev_col):
                    col_list.append(  [x, ] + prev_col    )

        col_map[size] = col_list

    return col_map[size]


def get_beta(size):
    if not size in beta_map:
        prev_list = get_beta(size-1)
        col_list = column_list(size)

        new_prev_list = []

        for prev in prev_list:
            new_prev = []
            for row in prev:
                new_row = []
                for x in row:
                    if x > 0:
                        new_row.append(x+1)
                    else:
                        new_row.append(0)
                new_prev.append(new_row)
            new_prev_list.append(new_prev)

        beta_list = []

        for col in col_list:
            for prev in new_prev_list:
                #max_row = get_max_row(prev)

                if is_compatible_with_prev(col, prev):
                    beta_list.append(  [ col,] + prev )


        beta_map[size] = beta_list

    return beta_map[size]

def get_max_row(triangle):
    max_row = [x for x in triangle[0]]

    for i in range(1, len(triangle)):
        row = triangle[i]
        for j in range(len(row)):
            if row[j] > max_row[j]:
                max_row[j] = row[j]

    return max_row


def get_catalan_column(col):
    cat = []

    for i in range(len(col)):
        if col[i] == 0:
            cat.append(i+1)
        else:
            cat.append(col[i])

    cat = sorted(cat)

    return cat


# Here are the rules!
# - nonzero entries in a row are weakly decreasing
# - columns are strictly increasing
# - if T[i,j] is 0 then every entry below it is strictly larger than
#   the smallest nonzero entry to the left of it
def is_compatible_with_prev(big, prev):
    min_row = [ x for x in prev[0]]
    for i in range(1, len(prev)):
        row = prev[i]
        for j in range(len(row)):
            if min_row[j] == 0 and row[j] > 0:
                min_row[j] = row[j]

    big_row_level = size

    for i in range(len(min_row)):
        if big[i] > 0 and min_row[i] > 0 and  big[i] >= min_row[i]:
            # column nonzero entries not decreasing
            return False
        elif big[i] == 0 and min_row[i] > 0:
            if big_row_level  >= min_row[i]:
                # this entry was available for big
                return False
        elif big[i] > 0:
            # update the level
            big_row_level = big[i]

    return True



if __name__ == '__main__':

    num = 0

    small_list = column_list(1)
    big_list = column_list(2)

    for x in range(1,8):
        print(len(column_list(x)))

    # count = 0
    #
    # for s in small_list:
    #     for b in big_list:
    #         if is_compatible(s,b):
    #             print(s,b)
    #             count+=1
    #         else:
    #             print('fail', s, b)
    #
    #
    # print(count)

    #big = [1,1,3]
    #small = [1,1]

    #print(is_compatible(small, big))


    size = 3

    tri_list = get_beta(size)

    layer_list = binary_layers.get_binary_layers(size)

    # for t in tri_list:
    #     util.print_array(t)

    print('num triangles', len(tri_list))

    tri_str_list = [str(t) for t in tri_list]
    bl_str_list = [str(b) for b in layer_list]

    print('#########')
    for b in bl_str_list:
        if str(b) not in tri_str_list:
            print('missing', b)



    # for t in tri_str_list:
    #     print(t)
    # print('----')
    # for b in layer_list:
    #     print(b)

    print('#########')
    for t in tri_str_list:
        if t not in bl_str_list:
            print('extra', t)

    #print(is_compatible_with_prev([1, 1, 1, 1], [[2, 0, 2], [3, 3], [4]]))

