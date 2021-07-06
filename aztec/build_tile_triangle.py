import triangle.array_util as util

import aztec.binary_layers_catalan as blc



row_dict = dict()
row_dict[1] =[[k, ] for k in range(0, 2)]
row_dict[0] = [(0,), ]


def get_row(size):
    if size not in row_dict:
        row_list = []
        prev_list = get_row(size-1)
        for idx in range(size+1):
            for prev in prev_list:
                if idx == 0 or idx > max(prev):
                    row_list.append([idx,] + prev)

        row_dict[size] = row_list

    return row_dict[size]


tt_dict = dict()
tt_dict[1] = [[[k, ],] for k in range(0,2)]

def get_tile_triangle(size):
    if not size in tt_dict:
        new_list = []
        prev_list = get_tile_triangle(size-1)
        row_list = get_row(size)

        for row in row_list:
            for prev in  prev_list:
                is_compatible = True

                if sum(prev[0]) > 0 and sum(row) == 0:
                    is_compatible = False
                else:
                    for idx in range(len(prev)):
                        if row[idx] == 0:
                            if prev[0][idx] > 0 and not any( x >= prev[0][idx] for x  in row[idx:len(row)]):
                                is_compatible = False
                                break
                        elif prev[0][idx] >= row[idx]:
                            is_compatible = False
                            break

                if is_compatible:
                    new_list.append([row] + prev)

        tt_dict[size] = new_list

    return tt_dict[size]


def replace_zeros_list(tri_list):
    return [ replace_zeros(triangle) for triangle in tri_list]

def replace_zeros(triangle):
    new_triangle = [[x for x in row] for row in triangle]

    for row in new_triangle:
        current_max = 0
        for idx in reversed(range(len(row))):
            if row[idx] > current_max:
                current_max = row[idx]
            elif row[idx] == 0 and current_max > 0:
                row[idx] = current_max

    return new_triangle


if __name__ == '__main__':

    size = 3

    tri_list = get_tile_triangle(size)

    #blc_list = blc.get_binary_layers(size)

    print('xxxxxxxxxxxxxxxx')

    for t in tri_list:
        util.print_array(t)
        util.print_array(replace_zeros(t))
        print('===============')


    # for b in blc_list:
    #     if not b in tri_list:
    #         util.print_array(b)

    print(len(tri_list))

    util.print_block_totals(tri_list)

    my_tri_lists = [get_tile_triangle(2), get_tile_triangle(3), get_tile_triangle(4)]
    my_totals = [util.print_block_totals(x) for x in my_tri_lists]
    print('block totals=', my_totals)


    t = tri_list[50]
    max_t = tri_list[-1]

    util.get_mma_block_pyramid(t, max_t)