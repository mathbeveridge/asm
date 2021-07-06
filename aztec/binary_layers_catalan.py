import aztec.binary_comb as binary_comb
import triangle.array_util as util
import triangle.build_binary_triangle as bbt
import stackset.build_stack_set as bss

def get_binary_layers(size):

    bin_list = binary_comb.get_binary_triangle(size)
    layer_list = []

    #bin_list = [ bin_list[6] ]

    for b in bin_list:
        print(b)
        layer_list.append(get_catalan_layers(b))

    return layer_list


def get_catalan_layers(bin_tri):
    # reverse it
    triangle = [[x for x in row] for row in reversed(bin_tri)]
    # flip it
    #triangle = util.flip_triangle2(triangle)

    temp =  get_catalan_layers_impl(triangle)

    ret_val = [[x+1 for x in row] for row in temp]

    print('input', bin_tri, 'output', ret_val)


    return ret_val


def get_catalan_layers_impl(bin_tri_reversed):
    print('\timpl input', bin_tri_reversed)

    # we can change this one
    triangle = [[x for x in row] for row in bin_tri_reversed]

    if len(triangle) == 1:
        if triangle[0][0] == 1:
            return [[0,],]
        else:
            return [[-1, ], ]

    # OTHERWISE:

    util.print_array(triangle)

    #triangle = util.flip_triangle2(triangle)
    size = len(triangle)

    layer = []

    # find index of last one in each row
    for row in triangle:
        if 1 in row:
            layer.append(len(row) - 1 - row[::-1].index(1))
        else:
            layer.append(-1)

    # check whether it is "supported" by a one in another row.
    for idx,val in enumerate(layer):
        if val > -1:
            if idx < len(layer)-1 and any(x >= val for x in layer[idx+1: len(layer)]):
                # can't take it yet
                layer[idx]= -1
            else:
                # take it away from the triangle.
                print(triangle, idx, val)
                triangle[idx][val] = 0

    new_triangle = [[x for x in row[0:len(row)-1]] for row in triangle[0:len(triangle)-1]]

    layers = get_catalan_layers_impl(new_triangle)

    layers.insert(0,layer)

    return layers


if __name__ == '__main__':

    size = 2

    layered_list = get_binary_layers(size)



    for x in layered_list:
        util.print_array(x)

    print(len(layered_list))