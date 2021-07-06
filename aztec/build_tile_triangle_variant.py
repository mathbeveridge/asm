# replace 0's with biggest seen before it.

import triangle.array_util as util

import aztec.build_tile_triangle as btt




row_dict = dict()
row_dict[1] =[[k, ] for k in range(0, 2)]
row_dict[0] = [(0,), ]


# rows weakly decreasing
def get_row(size):
    if size not in row_dict:
        row_list = []
        prev_list = get_row(size-1)
        for idx in range(size+1):
            for prev in prev_list:
                if idx >= prev[0]:
                    row_list.append([idx,] + prev)

        row_dict[size] = row_list

    return row_dict[size]



tt_dict = dict()
tt_dict[1] = [[[k, ],] for k in range(0,2)]

# columns weakly decreasing and
# if T(i,j) = T(i+1,j) then T(i,j) = T(i,j+1)

def get_tile_triangle(size):
    if not size in tt_dict:
        new_list = []
        prev_list = get_tile_triangle(size-1)
        row_list = get_row(size)

        for row in row_list:
            for prev in  prev_list:
                is_compatible = True

                prev_row = prev[0]

                for idx in range(len(prev_row)):
                    if row[idx] < prev_row[idx]:
                        is_compatible = False
                        break
                    elif row[idx] == prev_row[idx] and not row[idx] == row[idx+1]:
                        is_compatible = False
                        break


                if is_compatible:
                    new_list.append([row] + prev)

        tt_dict[size] = new_list

    return tt_dict[size]



if __name__ == '__main__':

    size = 4

    #orig_list = btt.get_tile_triangle(size)
    #orig_list2 = btt.replace_zeros_list(orig_list)

    variant_list = get_tile_triangle(size)

    # print('variant only')
    # for t in variant_list:
    #     if t not in orig_list2:
    #         util.print_array(t)
    #
    # print('original only')
    # for t in orig_list2:
    #     if t not in variant_list:
    #         util.print_array(t)

    print(len(variant_list))


    #for t in orig_list:
    #    util.print_array(t)

    util.print_block_totals(variant_list)