import aztec.build_bigog as build_bigog
import triangle.build_binary_triangle as build_binary
import triangle.array_util as util

def jeu_de_toquin(bin_star_triangle):
    size = len(bin_star_triangle)

    triangle = bin_star_triangle

    for col_idx in reversed(range(size)):
        print('processing column', col_idx)
        # note: don't need to process the rightmost diagonal entries
        for row_idx in reversed(range(size - 1 - col_idx)):
            print('\tprocessing entry', row_idx, col_idx)
            triangle = jt_move(triangle,row_idx,col_idx)

    return triangle


def jt_move(triangle, row_idx, col_idx):

    print('\t\tjt_move', row_idx, col_idx, triangle)

    if not col_idx < len(triangle[row_idx]) -1:
        raise IndexError("Called jt_move for ({0},{1}) on {2})".format(str(row_idx), str(col_idx), str(triangle)))

    s = triangle[row_idx][col_idx]
    x = triangle[row_idx][col_idx+1]
    y = triangle[row_idx+1][col_idx]


    if s <= x and s <= y:
        # all is good
        new_triangle = triangle
        new_row_idx = row_idx
        new_col_idx = col_idx
    else:
        new_triangle = util.clone_array(triangle)

        if x < s:
            #if not y <= x:
            #    raise ValueError("Programming error y>x for ({0},{1}) on {2})".format(str(row_idx), str(col_idx), str(triangle)))

            new_triangle[row_idx][col_idx] = x
            new_triangle[row_idx][col_idx+1] = s
            new_row_idx = row_idx
            new_col_idx = col_idx + 1
        else:
            new_triangle[row_idx][col_idx] = y+1
            new_triangle[row_idx][col_idx+1] = x-1
            new_triangle[row_idx+1][col_idx] = s
            new_row_idx = row_idx + 1
            new_col_idx = col_idx

    if new_row_idx == row_idx and new_col_idx == col_idx:
        return new_triangle
    elif new_col_idx == len(triangle[new_row_idx]) - 1:
        return new_triangle
    else:
        return jt_move(new_triangle, new_row_idx, new_col_idx)

size = 3

bin_star_list = build_binary.get_binary_star_triangle(size)
bigog_list = build_bigog.get_bigog(size)


bin_star_list = [ [[0, 2, 3], [1, 2], [0]] ]

out_set = set()

for b in bin_star_list:

    x = jeu_de_toquin(b)
    print('in ', b)
    print('out', x)
    if not x in bigog_list:
        print('>>>>>>>>>>>>>> ERROR NOT BIGOG', x)
    out_set.add(str(x))
    print('==================')


print(len(out_set))